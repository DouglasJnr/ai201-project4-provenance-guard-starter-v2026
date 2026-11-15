#!/usr/bin/env python3
"""
Measure the cost of one run: a submission that goes all the way through
/submit → /appeal → /review.

    python measure_cost.py                 # 10 runs, writes results/cost_<date>.md
    python measure_cost.py --runs 20

This service makes no API calls, so there's no money or token spend. Its real
cost is compute: the seconds a run takes and the CPU it uses, most of it
spent running the local language model. That's what this measures.

How:
  - One run is the full path a contested submission takes:
        1. POST /submit   scored by both signals, labelled, logged
        2. POST /appeal   the writer disputes it, so it moves to under_review
        3. POST /review   a reviewer (with the token) resolves it. Runs
                          alternate between overturned and upheld
    Each step must return 200, or the measurement stops.
  - The real Flask app is called in-process through Flask's test client, so
    every step goes through the same code as a curl request. Only the HTTP
    socket is skipped, which takes well under a millisecond on loopback.
  - Run 0 is the cold start, when the model loads into memory. It's reported
    on its own and left out of the averages, because it happens once per
    server start, not once per run.
  - Each of the N warm runs records:
        wall     time.perf_counter() around the whole run, and per step
        cpu      time.process_time() around the whole run. This is CPU time
                 summed over all threads; torch runs on several cores.
        model    time inside detector.model_signal
        style    time inside stylometry.style_signal
  - Two inputs: a typical submission (a sample from samples/) and a worst case
    padded past DETECTOR_MAX_TOKENS, since the model never reads more than
    400 tokens.
  - Each run is logged to its own file, logs/cost_<date>.jsonl, with the same
    timestamp as results/cost_<date>.md: 3 entries per run (decided, appeal,
    review). Benchmark runs stay out of logs/audit.jsonl (the record of real
    requests) but are still on record. Each run uses its own creator_id
    (cost_*), so the rate limit never triggers.
  - /appeal and /review read the whole log to find the item, so their cost
    grows with the size of the log. The cost log is small, so the report also
    times one such lookup against the real logs/audit.jsonl. This is
    read-only: nothing is written to it.

Failed runs:
  - If any step of a run doesn't return 200, the run is recorded as failed.
    The report shows which step failed and with what status. Failed runs are
    counted and listed but left out of the averages, and measuring carries on.
  - Separately, each way a request can fail is triggered N times and
    measured: the status it returns, its wall and CPU time, and how many log
    lines it added. The expected answer is exactly one: a failure must leave a
    record. Two failures can't be triggered with a normal request, so they
    are simulated by temporarily replacing a function:
        crash after the model   stylometry.style_signal raises, so /submit
                                returns 500 after the model has already run
        detector unavailable    detector.model_signal raises
                                DetectorUnavailable, so /submit returns 503
"""

import argparse
import datetime as dt
import json
import platform
import resource
import statistics
import subprocess
import sys
import time

import config


def cpu_name() -> str:
    try:
        return subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:  # noqa: BLE001 - not macOS
        return platform.processor() or platform.machine()


def timed(fn, bucket: list):
    """Wrap fn so each call's duration is appended to bucket."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            bucket.append(time.perf_counter() - start)
    return wrapper


def summary(values):
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
    }


ROWS = (
    ("wall", "**whole run, wall seconds**"),
    ("cpu", "whole run, CPU seconds"),
    ("submit", "1. /submit"),
    ("model", "  ↳ model signal"),
    ("style", "  ↳ style signal"),
    ("appeal", "2. /appeal"),
    ("review", "3. /review"),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--sample", default="samples/clearly_ai.json")
    args = parser.parse_args()

    if not config.REVIEWER_TOKEN:
        sys.exit("No REVIEWER_TOKEN set, so /review is off and a run can't finish. "
                 "Create .env first (RUNNING.md, step 3).")

    # Benchmark runs get their own log, next to the real one. Set before app is
    # imported, so every write goes here.
    real_log = config.AUDIT_LOG
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    run_log = config.LOG_DIR / f"cost_{stamp}.jsonl"
    config.AUDIT_LOG = run_log

    import app as service
    import audit
    import detector
    import stylometry

    model_times, style_times = [], []
    detector.model_signal = timed(detector.model_signal, model_times)
    stylometry.style_signal = timed(stylometry.style_signal, style_times)
    client = service.app.test_client()
    review_headers = {"X-Reviewer-Token": config.REVIEWER_TOKEN}

    typical = json.loads((config.ROOT / args.sample).read_text(encoding="utf-8"))["text"]
    worst = (typical + " ") * 10   # well past 400 tokens; the model truncates
    inputs = [("typical", typical), ("worst case (400 tokens)", worst)]

    class StepFailed(Exception):
        def __init__(self, path, status, body):
            super().__init__(f"{path} → {status}")
            self.path, self.status, self.body = path, status, body

    def step(path, body, headers=None):
        start = time.perf_counter()
        response = client.post(path, json=body, headers=headers or {})
        elapsed = time.perf_counter() - start
        if response.status_code != 200:
            raise StepFailed(path, response.status_code, response.get_json(silent=True) or {})
        return response.get_json(), elapsed

    def one_run(text, creator, outcome):
        """A full run. On failure, returns a record of where it failed, not a crash."""
        model_times.clear(); style_times.clear()
        cpu0, wall0 = time.process_time(), time.perf_counter()
        times, cid = {}, None
        try:
            submitted, times["submit"] = step("/submit", {"text": text, "creator_id": creator})
            cid = submitted["content_id"]
            _, times["appeal"] = step("/appeal", {"content_id": cid,
                                                  "reasoning": "Cost measurement: appeal step."})
            reviewed, times["review"] = step("/review", {"content_id": cid,
                                                         "reviewer_id": "cost_reviewer",
                                                         "outcome": outcome,
                                                         "note": "Cost measurement: review step."},
                                             review_headers)
            if audit.current_status(cid) != outcome or reviewed["status"] != outcome:
                raise StepFailed("/review", 200, {"reason": f"status is not {outcome!r}"})
            failed = None
        except StepFailed as exc:
            failed = f"{exc.path} → {exc.status} {exc.body.get('reason') or exc.body.get('error', '')}"
        return {"wall": time.perf_counter() - wall0, "cpu": time.process_time() - cpu0,
                "submit": times.get("submit", 0.0), "appeal": times.get("appeal", 0.0),
                "review": times.get("review", 0.0), "model": sum(model_times),
                "style": sum(style_times), "content_id": cid or "—", "outcome": outcome,
                "failed": failed}

    print("Cold start (loads the model)…")
    cold = one_run(typical, "cost_cold", "overturned")
    if cold["failed"]:
        sys.exit(f"The cold-start run failed ({cold['failed']}); nothing to measure.")

    _, tokenizer = detector._load()
    results = []
    for name, text in inputs:
        tokens = min(len(tokenizer(text)["input_ids"]), config.DETECTOR_MAX_TOKENS)
        runs = []
        for i in range(1, args.runs + 1):
            outcome = "overturned" if i % 2 else "upheld"
            runs.append(one_run(text, f"cost_{name.split()[0]}_{i}", outcome))
            r = runs[-1]
            print(f"  {name:24} run {i:2}: {r['wall']:.3f}s  "
                  f"(submit {r['submit']:.3f} / appeal {r['appeal']:.3f} / review {r['review']:.3f})"
                  + (f"  FAILED {r['failed']}" if r["failed"] else ""))
        results.append((name, text, tokens, runs))

    # ── Failure cases: what each kind of failure costs, and does it leave a line?
    def log_count():
        return len(audit.read_entries())

    def failure(label, expected, send, before_each=None, reset_limits=True):
        rows = []
        for i in range(args.runs):
            # Bodies with no usable creator_id are rate-limited by IP, so ten in a
            # row would turn into 429s. Reset so each case measures its own failure.
            if reset_limits and hasattr(service.limiter, "reset"):
                service.limiter.reset()
            if before_each:
                before_each(i)
            n0 = log_count()
            model_times.clear()
            cpu0, wall0 = time.process_time(), time.perf_counter()
            response = send(i)
            wall, cpu = time.perf_counter() - wall0, time.process_time() - cpu0
            new = audit.read_entries()[n0:]
            rows.append({"status": response.status_code, "wall": wall, "cpu": cpu,
                         "model": sum(model_times), "lines": len(new),
                         "logged": ", ".join(f"{e.get('event') or e.get('status')}:"
                                             f"{e.get('reason') or e.get('error_type') or ''}"
                                             for e in new)})
        statuses = sorted({r["status"] for r in rows})
        ok = statuses == [expected] and all(r["lines"] == 1 for r in rows)
        print(f"  {label:40} {statuses} {'ok' if ok else 'MISMATCH'}")
        return {"label": label, "expected": expected, "rows": rows, "ok": ok}

    def post(path, **kw):
        return lambda i: client.post(path, **kw)

    # Items to point review failures at: one decided-only, one already reviewed.
    decided_only = client.post("/submit", json={"text": typical, "creator_id": "cost_fail_setup_a"}).get_json()["content_id"]
    done = client.post("/submit", json={"text": typical, "creator_id": "cost_fail_setup_b"}).get_json()["content_id"]
    client.post("/appeal", json={"content_id": done, "reasoning": "setup"})
    client.post("/review", json={"content_id": done, "reviewer_id": "cost_reviewer", "outcome": "upheld",
                                 "note": "setup"}, headers=review_headers)
    good_review = {"reviewer_id": "cost_reviewer", "outcome": "upheld", "note": "Cost measurement."}

    print("\nFailure cases…")
    failures = [
        failure("/submit body is a JSON array", 400,
                post("/submit", data='["text"]', content_type="application/json")),
        failure("/submit text under 3 words", 400,
                lambda i: client.post("/submit", json={"text": "too short", "creator_id": f"cost_fail_short_{i}"})),
        failure("/submit creator_id is an object", 400,
                post("/submit", json={"text": typical, "creator_id": {"id": "x"}})),
        failure("/submit over the rate limit", 429,
                lambda i: client.post("/submit", json={"text": "a", "creator_id": "cost_fail_flood"}),
                # use up this creator's 5/minute allowance once, before the first measured request
                before_each=lambda i: [client.post("/submit", json={"text": "a", "creator_id": "cost_fail_flood"})
                                       for _ in range(config.RATE_LIMIT_PER_MINUTE)] if i == 0 else None,
                reset_limits=False),
        failure("/appeal unknown content_id", 404,
                post("/appeal", json={"content_id": "c_doesnotexist", "reasoning": "x"})),
        failure("/review wrong token", 401,
                post("/review", json={"content_id": decided_only, **good_review},
                     headers={"X-Reviewer-Token": "wrong"})),
        failure("/review item never appealed", 409,
                post("/review", json={"content_id": decided_only, **good_review}, headers=review_headers)),
        failure("/review item already reviewed", 409,
                post("/review", json={"content_id": done, **good_review}, headers=review_headers)),
    ]

    # Simulated: these can't be caused by a normal request.
    real_style, real_model = stylometry.style_signal, detector.model_signal

    def broken_style(text):
        raise RuntimeError("simulated crash in style signal")
    stylometry.style_signal = broken_style
    failures.append(failure("/submit crashes after the model ran (sim.)", 500,
                            lambda i: client.post("/submit", json={"text": typical,
                                                                   "creator_id": f"cost_fail_crash_{i}"})))
    stylometry.style_signal = real_style

    def no_detector(text):
        raise detector.DetectorUnavailable("simulated: model can't load")
    detector.model_signal = no_detector   # not timed: the model never runs here
    failures.append(failure("/submit detector unavailable (sim.)", 503,
                            lambda i: client.post("/submit", json={"text": typical,
                                                                   "creator_id": f"cost_fail_nodet_{i}"})))
    detector.model_signal = real_model

    # How long one lookup takes on the real log (read-only).
    config.AUDIT_LOG = real_log
    real_lines = len(audit.read_entries())
    lookups = []
    for _ in range(10):
        start = time.perf_counter()
        audit.entries_for("c_cost_lookup_probe")
        lookups.append(time.perf_counter() - start)
    config.AUDIT_LOG = run_log
    lookup_ms = statistics.mean(lookups) * 1000

    peak_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_mb = peak_mb / 1024 / 1024 if sys.platform == "darwin" else peak_mb / 1024

    import torch
    out = config.RESULTS_DIR / f"cost_{stamp}.md"
    log_lines = len(audit.read_entries())
    lines = [
        f"# Cost of one run (submit → appeal → review) — {stamp}",
        "",
        f"- Machine: {cpu_name()}, {platform.system()} {platform.release()}, "
        f"torch {torch.__version__} on CPU with {torch.get_num_threads()} threads",
        f"- Model: `{config.DETECTOR_MODEL}`, max {config.DETECTOR_MAX_TOKENS} tokens",
        f"- Warm runs per input: {args.runs}, alternating overturned / upheld. "
        f"Method: see the docstring of `measure_cost.py`",
        f"- Cold start (first run, model loads): **{cold['wall']:.2f}s** wall, "
        f"{cold['cpu']:.2f}s CPU (submit {cold['submit']:.2f}s, appeal {cold['appeal']:.3f}s, "
        f"review {cold['review']:.3f}s). Not included in the averages below",
        f"- Peak memory of the process: **{peak_mb:.0f} MB**",
        f"- One log lookup (what /appeal and /review each do) on the real "
        f"`logs/audit.jsonl` ({real_lines} entries): **{lookup_ms:.1f} ms**, "
        f"mean of 10. It grows with the size of the log",
        f"- Log of every run: `{run_log.relative_to(config.ROOT)}` ({log_lines} entries, "
        f"3 per completed run, plus the failure cases below; creator_ids `cost_cold`, "
        f"`cost_typical_N`, `cost_worst_N`, `cost_fail_*`)",
        "",
    ]
    for name, text, tokens, runs in results:
        ok_runs = [r for r in runs if not r["failed"]]
        failed_runs = [r for r in runs if r["failed"]]
        lines += [
            f"## {name}: {len(text.split())} words, {tokens} tokens read by the model",
            "",
            f"Completed runs: **{len(ok_runs)} of {len(runs)}**. "
            f"Failed runs: **{len(failed_runs)}**, listed below and left out of the averages.",
            "",
        ]
        if ok_runs:
            s = {k: summary([r[k] for r in ok_runs]) for k, _ in ROWS}
            lines += ["| seconds | mean | median | min | max | stdev |",
                      "|---|---|---|---|---|---|"]
            for key, label in ROWS:
                v = s[key]
                lines.append(f"| {label} | {v['mean']:.4f} | {v['median']:.4f} | "
                             f"{v['min']:.4f} | {v['max']:.4f} | {v['stdev']:.4f} |")
            share = s["model"]["mean"] / s["wall"]["mean"] * 100
            lines += ["", f"Model signal share of the whole run: {share:.1f}%", ""]
        lines += ["| run | content_id | outcome | wall | CPU | submit | model | appeal | review | result |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(runs, 1):
            lines.append(f"| {i} | `{r['content_id']}` | {r['outcome']} | {r['wall']:.4f} | "
                         f"{r['cpu']:.4f} | {r['submit']:.4f} | {r['model']:.4f} | "
                         f"{r['appeal']:.4f} | {r['review']:.4f} | "
                         f"{'FAILED at ' + r['failed'] if r['failed'] else 'ok'} |")
        lines.append("")

    lines += [
        "## Failed requests: what each kind of failure costs",
        "",
        f"Each case was sent {args.runs} times. **Logged lines** is how many entries each "
        "request added to the log; it should always be 1, so that no failure goes "
        "unrecorded. (sim.) means simulated, by temporarily replacing a function, "
        "because the failure can't be caused by a normal request.",
        "",
        "| failure | expected | got | mean wall s | mean CPU s | model ran? | logged lines | logged as | verdict |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for f in failures:
        rows = f["rows"]
        got = ", ".join(str(c) for c in sorted({r["status"] for r in rows}))
        lines_added = sorted({r["lines"] for r in rows})
        logged_as = sorted({r["logged"] for r in rows})
        model_ran = "yes" if any(r["model"] > 0 for r in rows) else "no"
        lines.append(
            f"| {f['label']} | {f['expected']} | {got} | "
            f"{statistics.mean(r['wall'] for r in rows):.4f} | "
            f"{statistics.mean(r['cpu'] for r in rows):.4f} | {model_ran} | "
            f"{'/'.join(map(str, lines_added))} each | {'; '.join(logged_as)} | "
            f"{'ok' if f['ok'] else '**MISMATCH**'} |")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out}")
    print("\n".join(lines[2:10]))
    for name, _, _, runs in results:
        ok_runs = [r for r in runs if not r["failed"]]
        if ok_runs:
            s = {k: summary([r[k] for r in ok_runs])["mean"] for k, _ in ROWS}
            print(f"{name}: {len(ok_runs)}/{len(runs)} completed, mean {s['wall']:.3f}s wall, "
                  f"{s['cpu']:.3f}s CPU (submit {s['submit']:.3f}, appeal {s['appeal']:.4f}, "
                  f"review {s['review']:.4f})")
        else:
            print(f"{name}: 0/{len(runs)} completed")
    print(f"failure cases: {sum(f['ok'] for f in failures)}/{len(failures)} ok")


if __name__ == "__main__":
    main()
