# Running Provenance Guard

Everything about how the starter works.

This is a **web service**. It runs on your machine and you talk to it with
`curl` from another terminal. If you've not built a backend before, that's
assumed — the starter ships one that already answers.

### 1. What you need

| | |
|---|---|
| Python | 3.11, 3.12 or 3.13. **Not 3.14**: the pinned packages break on it |
| Disk | about 9 GB free (mostly `torch`, plus about 550 MB for the model) |
| RAM | 4 GB or more |
| Network | only for the first install and model download. After that it runs offline |
| Tools | `git` and `curl`. `jq` is optional, for reading the log |

### 2. Install

```bash
git clone https://github.com/DouglasJnr/ai201-project4-provenance-guard-starter-v2026 
cd ai201-project4-provenance-guard-starter-v2026

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

python test.py                     # checks Python, packages, disk, RAM
python detector.py                 # downloads the model (~550 MB) and scores a sample
```

You're ready when `python test.py` passes and `python detector.py` prints a
`model_signal` score. Run `source .venv/bin/activate` again in **every new
terminal** before running anything else.

### 3. Create your `.env` file (reviewer token)

`POST /review` lets a human reviewer resolve an appeal, so it's protected by a
secret token. The token lives in a `.env` file, which is gitignored and so
**isn't in the repo**. You make your own:

```bash
echo "REVIEWER_TOKEN=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')" > .env
chmod 600 .env                     # macOS/Linux: only you can read it
```

`config.py` loads `.env` automatically when the service starts. Without a
token, `/review` answers `503 review_disabled`. The endpoint is locked rather
than left open, and everything else works normally. Never commit `.env` or
paste the token into a README or results file.

### 4. Start the service

**macOS: use port 5050.** On recent macOS versions, AirPlay Receiver also
listens on port 5000. Requests to `127.0.0.1:5000` usually still reach this
service, but `localhost:5000` can be routed to AirPlay instead, which answers
with a `403`. That's confusing to debug, so use a port nobody else wants.

```bash
PORT=5050 python app.py            # macOS
python app.py                      # Linux / Windows: port 5000 is usually free
```

On Windows PowerShell, set the port with `$env:PORT=5050; python app.py`.

The examples below use `5050`. If you're on 5000, change the port. Leave this
terminal running and open a second one, activating the venv there too. Then
check that the service is up:

```bash
curl http://127.0.0.1:5050/health
```

`"detector_loaded": false` is normal until the first submission. That first
submission takes 10–20 seconds while the model loads, and later ones should take a second or two.

### 5. Walk through every route

Load the token into this terminal so the commands below can use it without
you pasting it:

```bash
export $(grep REVIEWER_TOKEN .env)
```

**Submit some writing.** Note the `content_id` in the response.

```bash
curl -X POST http://127.0.0.1:5050/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I started working at the library last spring. Most of my job is putting books back on the shelves.", "creator_id": "demo_writer"}'
```

**Appeal the decision.** This is what the writer would do.

```bash
curl -X POST http://127.0.0.1:5050/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_PASTE_ID_HERE", "reasoning": "I wrote this myself about my own job."}'
```

**Resolve the appeal.** This is what the reviewer would do. `outcome` is either
`upheld`, which keeps the original verdict, or `overturned`, which marks the
text as the writer's own.

```bash
curl -X POST http://127.0.0.1:5050/review \
  -H "Content-Type: application/json" \
  -H "X-Reviewer-Token: $REVIEWER_TOKEN" \
  -d '{"content_id": "c_PASTE_ID_HERE", "reviewer_id": "demo_reviewer", "outcome": "overturned", "note": "Personal, specific detail; plain style explains the score."}'
```

**Read the log back:**

```bash
curl "http://127.0.0.1:5050/log?limit=5"
```

Windows PowerShell users: see the `curl.exe` note under
[Your first five minutes](#your-first-five-minutes).

### 6. The logs

Everything the service decides goes to **`logs/audit.jsonl`**, with one JSON
object per line. The log is append-only: nothing is ever edited or removed, so
an appeal or review is added as a new line after the original decision.

| `event` / `status` | Written when |
|---|---|
| `status: "decided"` | `/submit` scored a text. It has `model_score`, `style_score`, `combined_score`, `guess` and `label` |
| `event: "appeal"`, `status: "under_review"` | a writer appealed |
| `event: "review"`, `status: "upheld"` or `"overturned"` | a reviewer resolved an appeal. It has `reviewer_id`, `note`, `final_guess` and `final_label` |
| `event: "rejected"` | a request was refused. `reason` says why: `rate_limited`, `body_not_object`, `invalid_creator_id`, `invalid_text`, `text_too_short` or `detector_unavailable` |

Ways to read it:

```bash
curl "http://127.0.0.1:5050/log?limit=20"           # through the service
tail -f logs/audit.jsonl                             # watch it live while you send requests
grep '"c_PASTE_ID_HERE"' logs/audit.jsonl            # one submission's full history
jq -c 'select(.event == "rejected")' logs/audit.jsonl   # every rejected request (needs jq)
```

**The repo ships with the author's log.** It's committed on purpose as the
evidence behind the README. Your requests are added after the existing
entries. To start with an empty log, run:

```bash
python -c "import audit; print(audit.clear(), 'entries removed')"
```

This deletes your working copy of the log. You can get the original back at
any time with `git checkout logs/audit.jsonl`.

### 7. Re-run the evidence

With the service running in the first terminal, run these in the second one.
Each writes a dated report to `results/`. The scripts default to port 5000,
so on macOS add `--url http://127.0.0.1:5050`.

```bash
URL=http://127.0.0.1:5050

python run_attacks.py --set attack_set --url $URL --label rerun   # the full attack set
python run_attacks.py --flood 15 --url $URL                         # shows 200s turning into 429s
python run_eval.py --url $URL --label rerun                         # the five criteria, three trials
python run_appeals.py --url $URL --label rerun                      # the appeal path, three trials
```

The full attack set and the eval each take several minutes, because every
submission runs the model.

**Rate limits:** `/submit` allows 5 requests a minute and 100 a day per
`creator_id`. If a request has no usable `creator_id`, it counts against the
caller's IP address instead. You set these in `config.py`. Limits are kept in
memory, so **restarting the service resets them**. If a run starts getting
`429`s you didn't expect, wait a minute or restart `app.py`.

### 8. Keeping it local

By default the service listens on `127.0.0.1`, so only your own machine can
reach it. Leave it that way. Setting `HOST=0.0.0.0` exposes the service, the
audit log (through `GET /log`, which has no login) and the review endpoint to
your whole network.

### 9. Status codes you'll see

| Code | Meaning |
|---|---|
| `200` | Done |
| `400` | The request's shape is wrong. The `reason` and `message` fields say exactly what. Examples: the body isn't a JSON object, `text` has fewer than 3 words, `creator_id` isn't a string |
| `401` | `/review` without the right `X-Reviewer-Token` header |
| `404` | That `content_id` doesn't exist in the log |
| `409` | `/review` on something that isn't `under_review`, e.g. never appealed or already reviewed |
| `429` | The rate limit was hit. Wait a minute |
| `503` | `review_disabled`: no `REVIEWER_TOKEN` in `.env`. `detector_unavailable`: the model can't load, so run `python detector.py` |

---

## The starter guide

Everything below is the original course guide this project was built from.

---

## Before your first class

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**You're ready when `python test.py` passes.**

You'll see `[WARN] Detector model — not downloaded yet`:

```bash
python detector.py
```

That downloads about 550 MB and scores a sample.

> **No API key for this pair.** Nothing here calls a hosted service. The model
> that reads your text runs on your own laptop.

---

## Your first five minutes

Two terminals. In the first:

```bash
python app.py
```

In the second:

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

You should get JSON back. That's the whole idea of a web service — something
sent it data, it sent something back.

> **On Windows, use `curl.exe` and keep it on one line.**
>
> In PowerShell, `curl` is an alias for a different tool and the command above
> fails with `Cannot bind parameter 'Headers'` before it ever reaches your
> service. The `\` line breaks don't work there either. This does:
>
> ```powershell
> curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'
> ```
>
> Every `curl` command in this file and in the brief works the same way: swap
> `curl` for `curl.exe` and put it on one line. Git Bash needs no change.

**Leave `/ping` alone.** It's your control. When something breaks later, check
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself, and that's a help-channel question.

Then try the route you're going to build:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "some writing", "creator_id": "me"}'
```

In the original starter this returned a `501` saying it wasn't built yet. In
this repo `/submit` is built. A two-word text like the one above now gets a
`400 text_too_short`, because the service won't score fewer than 3 words.

---

## The routes

| Route | State | What it does |
|---|---|---|
| `POST /ping` | **works** | The example. Don't edit it |
| `GET /health` | **works** | Is the service up, is the model loaded |
| `GET /log` | **works** | The audit log, as JSON |
| `POST /submit` | **built** | Scores text with both signals, labels it, and logs the decision |
| `POST /appeal` | **built** | A writer disputes a decision, which moves it to `under_review` |
| `POST /review` | **built (extension)** | A reviewer with the token resolves an appeal as `upheld` or `overturned` |

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python app.py` | Runs the service |
| `python detector.py` | Downloads the model and scores a sample — **run before class** |
| `python detector.py "some text"` | Score one piece of text from the terminal |
| `python stylometry.py "some text"` | Your style measures, on one piece of text |
| `python run_attacks.py --set <folder>` | The attack set — **unit 8** |
| `python run_attacks.py --flood 15` | Push past your rate limit and print the status codes — **unit 8** |
| `python run_eval.py --label before` | Your five criteria, three trials — **unit 8** |
| `python run_appeals.py --label before` | The appeal path (criterion 4), three trials |

---

## Which piece goes with which milestone

### Unit 7 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Trace a submission on paper | Nothing to run |
| 2 | Write your criteria | `criteria.md` — all five are yours |
| 3 | The route, one signal, the log | `app.py::submit`, `detector.py`, `audit.py` |
| 4 | Second signal, combine, score | `stylometry.py`, `scoring.py::combine_signals` |
| 5 | Labels and the appeal path | `scoring.py::score_to_label`, `app.py::appeal` |
| 6 | Write it up | `README.md` |

### Unit 8 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Rate limiting and the full log | `config.py`, the decorator in `app.py` |
| 2 | Run the attack set | `run_attacks.py` |
| 3 | Run your own criteria | `scenarios.py`, `run_eval.py` |
| 4 | Verdicts and diagnoses | `README.md` |
| 5 | Fix one thing, re-run | `run_attacks.py --label after` |
| 6 | What's still broken | `README.md` |

---

## Building `/submit` in three passes

The ordering is deliberate. It's how you tell a broken route from a broken
signal.

**Milestone 3.** Return a hardcoded response. Confirm `curl` gets it back
**before** you add any logic. Then pull `text` and `creator_id` out. Then call
one signal. Then log it.

**Milestone 4.** Add the second signal. Combine them. Log both scores.

**Milestone 5.** Turn the score into a label.

> Test each signal from a terminal on its own before wiring it in. If you skip
> that you'll spend an hour not knowing whether the route or the signal is
> lying to you.

---

## Turning on rate limiting (unit 8)

Three steps:

1. In `config.py`, set `RATE_LIMITING_ENABLED = True` — or run with
   `AI201_RATE_LIMITS=1`.
2. Choose your numbers there.
3. In `app.py`, uncomment the `@limiter.limit(...)` line above `submit`.

Then push past your limit and watch for `429`:

```bash
python run_attacks.py --flood 15
```

That sends 15 submissions from one `creator_id` and prints the run of status
codes — `200 200 200 ... 429 429` — which is exactly what your README's **Rate
Limiting** section asks you to paste. It also writes `results/flood_<date>.md`.

The attack set can't do this for you. Every attack row submits under its own
`creator_id`, so a full attack run looks like forty-odd different callers and
never trips a limit however long it is.

No `429` at all? Either your limit is above 15 a minute, or rate limiting is
still off. `GET /health` reports which.

Rejections are logged for you. **An attack that shows up only as an absence is
one you'll never find** — a thousand requests that got a `429` and left no
trace look exactly like a quiet afternoon.

---

## Running it somewhere else (unit 9)

Unit 9 asks you to deploy one of your systems. **Read this before you pick
which one** — for this project the answer is already decided, and it isn't the
hosted one.

Flask's built-in server says "development server" on startup because that's
what it is. A real one comes from `gunicorn`, which is in
`requirements.txt` and unused until now:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Two settings do the work, and both read the environment:

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback — your machine only. A host needs `0.0.0.0`, or nothing outside the box can reach the service and it looks like the app is down |
| `PORT` | `5000` | Most hosts hand you a port in `PORT` and expect you to bind exactly that one |
| `AI201_DEBUG` | `1` | Debug mode. Off automatically whenever `HOST` isn't loopback — an interactive debugger on a public address is a stranger's Python prompt inside your process |

Nothing about your local workflow changes. With no variables set you get
`http://127.0.0.1:5000` and every `curl` above still works.

### This project will not fit a free host

Say it plainly, because the arithmetic is the point:

| What has to be in memory | Roughly |
|---|---|
| `torch` | ~200–800 MB depending on the build |
| the `gpt2` weights | ~550 MB on disk, loaded into RAM to score |
| Flask, gunicorn, your code | the rest |
| **A free tier gives you** | **512 MB** |

That's over budget before a single request arrives — and a free host has no
persistent disk, so the 550 MB download starts again after every idle
spin-down. There is no configuration that fixes this. The model is the size it
is.

**So pair 4 extensions take Path B — local, with logs.** That is the expected
answer for this project, not a fallback and not a failure. Working out that a
system doesn't fit its host *before* you spend an evening watching it get
killed is the skill unit 9 is actually testing. Write the arithmetic above in
your write-up; that's the deliverable.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting: thresholds, weights, rate limits, the model, and the reviewer token (loaded from `.env`) |
| `.env` | **Not in the repo — you create it.** Holds `REVIEWER_TOKEN`. Gitignored |
| `app.py` | The service and every route, including payload validation |
| `run_appeals.py` | Runs the appeal path three times |
| `detector.py` | Signal one — the local model. Given to you |
| `stylometry.py` | Signal two. **Stubs — you build these** |
| `scoring.py` | Combining and labelling. **Stubs — you build these** |
| `audit.py` | The audit log writer. Given to you |
| `run_attacks.py` | Runs the attack set — **unit 8** |
| `run_eval.py` | Runs your criteria three times — **unit 8** |
| `scenarios.py` | What your test runs. **You fill this in** |
| `criteria.md` | Your five criteria. **You write all five** |
| `logs/audit.jsonl` | Your audit log. **Commit it** |
| `results/` | Attack runs and run logs. **Commit them** |

---

## The two blind spots, up front

Both signals have one, and unit 8's attack set is built out of them. You have
to name them yourself in Milestone 1 — but knowing they exist now saves you
from being surprised.

**Signal one** measures how *predictable* your text is. Predictability isn't
authorship. What it really rewards is common words in short, ordinary
sentences — someone writing in a second language and staying with vocabulary
they're sure of, a younger writer, anyone writing plainly on purpose. Writing
like that scores about as machine-like as machine writing does. (Dense, ornate
prose often goes the other way and reads as human, because rare words are what
a language model fails to predict.) So the writers this signal is most likely
to accuse are the ones with the least room to argue back. That is the false
positive the whole project is about, and it's structural rather than a bug.

**Signal two** cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — typos, broken-up
sentences, a pasted quotation. That is very cheap to do on purpose.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `501 not_implemented` | Correct at the start — that's the TODO in `app.py` |
| `404` from curl | Is the server running? Is the path exactly what you typed? |
| `403` from curl on macOS | You reached AirPlay Receiver, which also listens on port 5000, not this service. Run `PORT=5050 python app.py` and use 5050 |
| `503 review_disabled` from `/review` | No `REVIEWER_TOKEN` in `.env`. See step 3 at the top |
| `401 unauthorized` from `/review` | The `X-Reviewer-Token` header is missing or doesn't match `.env`. Did you run `export $(grep REVIEWER_TOKEN .env)` in this terminal? |
| `Cannot bind parameter 'Headers'` | You're in PowerShell, where `curl` is a different tool. Use `curl.exe`, on one line |
| Request body arrives empty | curl needs `-H "Content-Type: application/json"` |
| `Address already in use` | A server left running from an earlier attempt. Kill it, don't debug it |
| The first submission takes 10+ seconds | Signal one is loading the model into memory. Later ones take a second or two |
| *Every* submission takes 10+ seconds | Something is reloading the model each call. `GET /health` shows `detector_loaded` — if it goes back to `false`, look for a reload in your handler |
| `DetectorUnavailable` | Run `python detector.py` once to download the model |
| `/appeal` seems to do nothing | Does the `content_id` you sent actually exist in the log? A typo there fails silently |
| Every request gets through, no `429` ever | The decorator is uncommented but limiting is still off. Set `RATE_LIMITING_ENABLED` in `config.py` |
| Flask-Limiter warns about storage | Shouldn't happen — `storage_uri` is preconfigured. If you changed it, put it back |
| All three of your labels never appear | Your ranges have a gap. `scoring.label_ranges()` prints them |

If the route won't respond, go back to `/ping`. If that answers, the problem is
in your handler.

---

## A note on committing

At least four new commits in unit 7, four more in unit 8.

`logs/` and `results/` are deliberately **not** in `.gitignore`. Your audit log
is evidence, and the entries you paste into your README are what unit 8 grades.

**Do not delete and recreate this repository.** You submit the same URL both
units.
