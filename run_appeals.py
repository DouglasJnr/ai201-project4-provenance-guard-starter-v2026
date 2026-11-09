#!/usr/bin/env python3
"""
Run criterion 4 — the appeal path — three times.

    python app.py                              # in one terminal
    python run_appeals.py --label before       # in another

`run_eval.py` only posts to /submit, and an appeal needs a real content_id
first, so this one is separate.

Each trial submits two fresh texts. The first gets a proper appeal. The second
gets five bad ones — unknown id, missing id, empty id, missing reasoning,
whitespace-only reasoning. After every request it records the HTTP status,
the response, any new lines in the audit log, and the second submission's
status, so you can check a bad appeal changed nothing.

Like run_eval.py, this records rather than judges. The verdict is yours.
"""

import argparse
import datetime as dt
import json
import sys

import config

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"
SAMPLE = config.ROOT / "samples" / "clearly_human.json"


def log_entries():
    """Every line of the audit log, read straight from the file the service writes."""
    if not config.AUDIT_LOG.exists():
        return []
    return [json.loads(line) for line in config.AUDIT_LOG.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def statuses(content_id):
    return [e.get("status") for e in log_entries() if e.get("content_id") == content_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    text = json.loads(SAMPLE.read_text(encoding="utf-8"))["text"]

    def submit(creator_id):
        response = requests.post(f"{args.url}/submit",
                                 json={"text": text, "creator_id": creator_id}, timeout=90)
        return response.json()["content_id"]

    def appeal(case, body, watched_id):
        before = len(log_entries())
        response = requests.post(f"{args.url}/appeal", json=body, timeout=30)
        return {
            "case": case,
            "sent": body,
            "http": response.status_code,
            "response": response.json() if response.content else {},
            "new_log_entries": log_entries()[before:],
            "watched_statuses_after": statuses(watched_id),
        }

    trials = []
    for trial in range(1, args.trials + 1):
        # A creator_id per submission, so the rate limit never gets involved.
        good = submit(f"eval_appeal_t{trial}_a")
        untouched = submit(f"eval_appeal_t{trial}_b")
        results = [
            appeal("valid appeal",
                   {"content_id": good, "reasoning": "I wrote this myself about my own week."}, good),
            appeal("unknown id",
                   {"content_id": "c_doesnotexist", "reasoning": "I wrote this."}, untouched),
            appeal("missing content_id", {"reasoning": "I wrote this."}, untouched),
            appeal("empty content_id", {"content_id": "", "reasoning": "I wrote this."}, untouched),
            appeal("missing reasoning", {"content_id": untouched}, untouched),
            appeal("whitespace reasoning", {"content_id": untouched, "reasoning": "   "}, untouched),
        ]
        trials.append({"trial": trial, "valid_id": good, "untouched_id": untouched,
                       "results": results})

        print(f"trial {trial}")
        for r in results:
            outcome = r["response"].get("status") or r["response"].get("error")
            logged = [e.get("event") for e in r["new_log_entries"]]
            print(f"  {r['case']:<22} {r['http']} {outcome:<13} "
                  f"logged={logged} watched={r['watched_statuses_after']}")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_run_{stamp}{label}.json"
    path.write_text(json.dumps({"run_at": stamp, "trials": trials}, indent=2), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
