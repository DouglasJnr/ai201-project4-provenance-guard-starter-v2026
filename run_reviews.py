#!/usr/bin/env python3
"""
Run capstone criteria 6-10, the /review extension, three times.

    python run_reviews.py                    # no server needed
    python run_reviews.py --label before
    python run_reviews.py --label after

What each criterion sends is written down in scenarios.py::REVIEW_SCENARIOS.
This file only runs it.

It runs in-process with Flask's test client rather than against `python
app.py`, for two reasons:

  - Criterion 10 has to make the service crash on purpose, by swapping one
    function for one that raises. That can only be done from inside the process.
  - The run gets its own log, logs/review_eval_<stamp>.jsonl, so evaluation
    traffic never lands in logs/audit.jsonl. It's still kept next to the real
    log, and the results file names it.

Criterion 9 still uses real threads, so the audit lock in /review is tested
the way the threaded server would use it.

Each case records the HTTP status, the response, every log line the request
added, and the item's status before and after. It marks whether the case did
what scenarios.py expected. Whether that adds up to a pass is the criterion's
call, and yours. The reviewer token is never written to the results.
"""

import argparse
import builtins
import datetime as dt
import json
import sys
import threading

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


def fill(value, content_id, token):
    """Swap the {content_id} and {token} placeholders, anywhere in a body."""
    if isinstance(value, str):
        return value.replace("{content_id}", content_id).replace("{token}", token)
    if isinstance(value, list):
        return [fill(v, content_id, token) for v in value]
    if isinstance(value, dict):
        return {k: fill(v, content_id, token) for k, v in value.items()}
    return value


def redact(value, token):
    """The same thing in reverse, so the real token never reaches a results file."""
    if not token:
        return value
    return json.loads(json.dumps(value).replace(token, "<REVIEWER_TOKEN>"))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    args = parser.parse_args()

    token = config.REVIEWER_TOKEN
    if not token:
        sys.exit("No REVIEWER_TOKEN set, so /review is off. Create .env first "
                 "(RUNNING.md, step 3).")

    import scenarios

    # Set before app is imported, so every write from this run goes here.
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    run_log = config.LOG_DIR / f"review_eval_{stamp}.jsonl"
    config.AUDIT_LOG = run_log

    import app as service
    import audit
    import detector
    import scoring
    import stylometry

    service.app.config["PROPAGATE_EXCEPTIONS"] = False   # a crash must become a 500
    client = service.app.test_client()
    good_headers = {"X-Reviewer-Token": token}
    modules = {"detector": detector, "stylometry": stylometry,
               "scoring": scoring, "audit": audit}
    counter = {"n": 0}

    print(f"Loading the model and running {args.trials} trial(s). Log: "
          f"{run_log.relative_to(config.ROOT)}")

    # ── helpers ───────────────────────────────────────────────────────────────

    def reset_limits():
        # Only /submit is limited, and every submit here has its own creator_id,
        # but reset anyway so one case can never make the next one a 429.
        if hasattr(service.limiter, "reset"):
            service.limiter.reset()

    def post(route, body, headers=None, test_client=None):
        reset_limits()
        response = (test_client or client).post(route, json=body, headers=headers or {})
        return response.status_code, response.get_json(silent=True) or {}

    def submit(text):
        counter["n"] += 1
        code, body = post("/submit", {"text": text,
                                      "creator_id": f"eval_review_{stamp}_{counter['n']}"})
        if code != 200:
            raise RuntimeError(f"setup /submit returned {code}: {body}")
        return body["content_id"], body["guess"]

    def make_item(state, text=scenarios.REVIEW_TEXT):
        """A fresh item in the state a case needs: decided, under_review or reviewed."""
        cid, guess = submit(text)
        if state in ("under_review", "reviewed"):
            code, body = post("/appeal", {"content_id": cid,
                                          "reasoning": scenarios.APPEAL_REASONING})
            if code != 200:
                raise RuntimeError(f"setup /appeal returned {code}: {body}")
        if state == "reviewed":
            code, body = post("/review", {"content_id": cid, "reviewer_id": "eval_reviewer",
                                          "outcome": "overturned",
                                          "note": "Setup: first review."}, good_headers)
            if code != 200:
                raise RuntimeError(f"setup /review returned {code}: {body}")
        return cid, guess

    def mark():
        return len(audit.read_entries())

    def since(n):
        return audit.read_entries()[n:]

    def item_lines(lines, cid):
        return [e for e in lines if e.get("content_id") == cid]

    # ── criterion 6 ───────────────────────────────────────────────────────────

    def criterion_6(sc):
        rows = []
        for r in sc["reviews"]:
            cid, original_guess = make_item("under_review", sc["texts"][r["text"] - 1])
            n = mark()
            code, body = post("/review", {"content_id": cid, "reviewer_id": "eval_reviewer",
                                          "outcome": r["outcome"], "note": r["note"]},
                              good_headers)
            new = since(n)
            reviews = [e for e in item_lines(new, cid) if e.get("event") == "review"]
            want_guess = original_guess if r["outcome"] == "upheld" else "human"
            status_after = audit.current_status(cid)
            ok = (code == 200 and body.get("final_guess") == want_guess
                  and status_after == r["outcome"] and len(reviews) == 1
                  and reviews[0].get("final_guess") == want_guess)
            rows.append({"case": f"{r['outcome']} (text {r['text']})", "content_id": cid,
                         "expect": f"200, final_guess={want_guess}", "http": code,
                         "original_guess": original_guess,
                         "final_guess": body.get("final_guess"),
                         "status_after": status_after, "review_lines": len(reviews),
                         "as_expected": ok, "response": body, "new_log_lines": new})
        return rows

    # ── criterion 7 ───────────────────────────────────────────────────────────

    def criterion_7(sc):
        rows = []
        for a in sc["auth"]:
            cid, _ = make_item("under_review")
            before = audit.current_status(cid)
            n = mark()
            code, body = post("/review", fill(sc["body"], cid, token),
                              fill(a["headers"], cid, token))
            new = since(n)
            after = audit.current_status(cid)
            reviews = [e for e in item_lines(new, cid) if e.get("event") == "review"]
            unauthorized = [e for e in new if e.get("reason") == "unauthorized"]
            token_leaked = token in json.dumps(new)
            ok = (code == sc["expect"] and before == after == "under_review"
                  and not reviews and len(unauthorized) == 1 and not token_leaked)
            rows.append({"case": a["case"], "content_id": cid, "expect": sc["expect"],
                         "http": code, "status_before": before, "status_after": after,
                         "review_lines": len(reviews),
                         "unauthorized_lines": len(unauthorized),
                         "token_in_log": token_leaked, "as_expected": ok,
                         "response": body, "new_log_lines": new})
        return rows

    # ── criterion 8 ───────────────────────────────────────────────────────────

    def criterion_8(sc):
        rows = []
        for c in sc["cases"]:
            cid, _ = make_item(c["on"])
            before = audit.current_status(cid)
            n = mark()
            headers = good_headers if c["route"] == "/review" else {}
            code, body = post(c["route"], fill(c["body"], cid, token), headers)
            new = since(n)
            after = audit.current_status(cid)
            changed = item_lines(new, cid)          # appeal or review lines for this item
            rejected = [e for e in new if e.get("event") == "rejected"]
            ok = (code == c["expect"] and before == after and not changed
                  and len(rejected) == 1)
            rows.append({"case": c["case"], "route": c["route"], "content_id": cid,
                         "expect": c["expect"], "http": code,
                         "status_before": before, "status_after": after,
                         "item_lines_added": len(changed), "rejected_lines": len(rejected),
                         "as_expected": ok, "response": body, "new_log_lines": new})
        return rows

    # ── criterion 9 ───────────────────────────────────────────────────────────

    def criterion_9(sc):
        rows = []
        for run in range(1, sc["runs"] + 1):
            cid, _ = make_item("under_review")
            n = mark()
            barrier = threading.Barrier(len(sc["outcomes"]))
            results = {}

            def send(outcome):
                own_client = service.app.test_client()
                barrier.wait()      # both threads leave here together
                results[outcome] = own_client.post(
                    "/review", headers=good_headers,
                    json={"content_id": cid, "reviewer_id": f"eval_reviewer_{outcome}",
                          "outcome": outcome, "note": f"Concurrent {outcome}."},
                ).status_code

            reset_limits()
            threads = [threading.Thread(target=send, args=(o,)) for o in sc["outcomes"]]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            new = since(n)
            reviews = [e for e in item_lines(new, cid) if e.get("event") == "review"]
            codes = sorted(results.values())
            ok = codes == [200, 409] and len(reviews) == 1
            rows.append({"case": f"run {run}", "content_id": cid,
                         "expect": "one 200 + one 409, 1 review line", "http": results,
                         "review_lines": len(reviews),
                         "status_after": audit.current_status(cid),
                         "as_expected": ok, "new_log_lines": new})
        return rows

    # ── criterion 10 ──────────────────────────────────────────────────────────

    def criterion_10(sc):
        rows = []
        for c in sc["crashes"]:
            module_name, func_name = c["patch"].split(".")
            module = modules[module_name]
            exc_type = getattr(builtins, c["raises"])

            cid = None
            if c["route"] == "/submit":
                body = {"text": scenarios.REVIEW_TEXT,
                        "creator_id": f"eval_review_{stamp}_crash_{len(rows) + 1}"}
                headers = {}
            elif c["route"] == "/appeal":
                cid, _ = make_item(c.get("on", "decided"))
                body = {"content_id": cid, "reasoning": scenarios.APPEAL_REASONING}
                headers = {}
            else:
                cid, _ = make_item(c.get("on", "under_review"))
                body = {"content_id": cid, "reviewer_id": "eval_reviewer",
                        "outcome": "overturned", "note": "This request will crash."}
                headers = good_headers

            def broken(*_args, **_kwargs):
                raise exc_type(f"simulated crash for criterion 10 ({c['case']})")

            before = audit.current_status(cid) if cid else None
            real = getattr(module, func_name)
            setattr(module, func_name, broken)
            # The app prints a traceback for every crash; these are on purpose,
            # and the audit log line is what this criterion checks.
            service.app.logger.disabled = True
            try:
                n = mark()
                code, response = post(c["route"], body, headers)
            finally:
                setattr(module, func_name, real)
                service.app.logger.disabled = False
            new = since(n)
            after = audit.current_status(cid) if cid else None
            errors = [e for e in new if e.get("event") == "error"]
            ok = (code == sc["expect"] and bool(response.get("error_id"))
                  and len(errors) == 1
                  and errors[0].get("error_id") == response.get("error_id")
                  and errors[0].get("error_type") == c["raises"]
                  and before == after
                  and not [e for e in new if e.get("event") in ("decided", "appeal", "review")
                           or e.get("status") == "decided"])
            rows.append({"case": c["case"], "route": c["route"], "content_id": cid,
                         "expect": sc["expect"], "http": code,
                         "error_id": response.get("error_id"),
                         "logged_error_type": errors[0].get("error_type") if errors else None,
                         "logged_where": errors[0].get("where") if errors else None,
                         "error_lines": len(errors), "status_before": before,
                         "status_after": after, "as_expected": ok,
                         "response": response, "new_log_lines": new})
        return rows

    runners = {6: criterion_6, 7: criterion_7, 8: criterion_8, 9: criterion_9,
               10: criterion_10}

    # ── run ───────────────────────────────────────────────────────────────────

    report = []      # one entry per scenario: {scenario, trials: [rows, rows, rows]}
    for sc in scenarios.REVIEW_SCENARIOS:
        print(f"\n{sc['criterion']}. {sc['name']}")
        trials = []
        for trial in range(1, args.trials + 1):
            rows = runners[sc["criterion"]](sc)
            trials.append(rows)
            hits = sum(r["as_expected"] for r in rows)
            print(f"  trial {trial}: {hits}/{len(rows)} as expected")
            for r in rows:
                if not r["as_expected"]:
                    print(f"    ✗ {r['case']}: expected {r['expect']}, got {r['http']}")
        report.append({"scenario": sc, "trials": trials})

    write_report(report, args, stamp, run_log, token)


def write_report(report, args, stamp, run_log, token):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"review_run_{stamp}{label}.md"
    n = args.trials

    lines = [
        f"# Review run{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_reviews.py` · scenarios: `scenarios.py::REVIEW_SCENARIOS`",
        "- Service: `app.py::review`, `app.py::appeal` (in-process, Flask test client)",
        f"- Log for this run: `{run_log.relative_to(config.ROOT)}`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Each cell is how many cases did what scenarios.py expected. Fill in",
        "Target from `criteria.md` and the Verdict yourself.",
        "",
        f"| Criterion | Target | {' | '.join(f'Run {i}' for i in range(1, n + 1))} | Verdict |",
        f"|---|---|{'|'.join(['---'] * n)}|---|",
    ]
    for entry in report:
        sc = entry["scenario"]
        cells = [f"{sum(r['as_expected'] for r in rows)}/{len(rows)}" for rows in entry["trials"]]
        lines.append(f"| {sc['criterion']}. {sc['name']} |  | {' | '.join(cells)} |  |")

    lines += ["", "---", "", "## Cases that didn't do what was expected", ""]
    misses = [(entry["scenario"], t, r) for entry in report
              for t, rows in enumerate(entry["trials"], 1) for r in rows if not r["as_expected"]]
    if not misses:
        lines.append("None.")
    else:
        lines += ["| Criterion | Trial | Case | Expected | Got |", "|---|---|---|---|---|"]
        for sc, t, r in misses:
            lines.append(f"| {sc['criterion']} | {t} | {r['case']} | {r['expect']} | "
                         f"{json.dumps(r['http'])} |")

    lines += ["", "---", "", "## What actually came back", "",
              "Real output, token redacted. The full log lines are in the log above.", ""]
    for entry in report:
        sc = entry["scenario"]
        lines += [f"### {sc['criterion']}. {sc['name']}", ""]
        for t, rows in enumerate(entry["trials"], 1):
            compact = [{k: v for k, v in r.items() if k != "new_log_lines"} for r in rows]
            lines += [f"**Trial {t}**", "", "```json",
                      json.dumps(redact(compact, token), indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print(f"Log   {run_log.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
