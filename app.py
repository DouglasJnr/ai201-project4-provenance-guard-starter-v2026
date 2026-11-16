#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import hmac
import uuid

from flask import Flask, jsonify, request

import audit
import config

app = Flask(__name__)


# ── Payload shape ─────────────────────────────────────────────────────────────
# One habit for every route: check the shape of the WHOLE payload before any
# other code touches it. Past this point, fields have the types the code
# expects, so neither a .get on a list nor a dict written to the log as a
# creator can happen.

def _json_object() -> dict | None:
    """The request body if it's a JSON object, otherwise None.

    get_json(silent=True) returns whatever parsed: a list, a string, a number,
    or None. Only a dict has .get.
    """
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else None


def _creator_for_log(payload: dict | None) -> str:
    """A creator_id that is safe to write to the log, whatever was sent.

    Only for rejection entries. Accepted submissions get a checked creator_id
    from _validate_submission.
    """
    creator = payload.get("creator_id") if payload is not None else None
    if isinstance(creator, str) and creator.strip():
        return creator.strip()[:config.CREATOR_ID_MAX_CHARS]
    return "unknown"


def _validate_submission(payload: dict | None):
    """Check every /submit field. Returns (text, creator_id, None) when valid,
    or (None, None, (reason, message)) for the first problem found."""
    if payload is None:
        return None, None, ("body_not_object",
                            'Send a JSON object like {"text": "...", "creator_id": "..."}.')

    creator_id = payload.get("creator_id")
    if creator_id is None:
        creator_id = "unknown"
    elif (not isinstance(creator_id, str) or not creator_id.strip()
          or len(creator_id.strip()) > config.CREATOR_ID_MAX_CHARS):
        return None, None, ("invalid_creator_id",
                            f'"creator_id" must be a non-empty string of at most '
                            f'{config.CREATOR_ID_MAX_CHARS} characters.')
    else:
        creator_id = creator_id.strip()

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        return None, None, ("invalid_text", 'Send JSON with a non-empty "text" string.')

    # Prevents detector.perplexity's "fewer than 3 tokens" ValueError.
    if len(text.split()) < config.SUBMIT_MIN_WORDS:
        return None, None, ("text_too_short",
                            f'"text" needs at least {config.SUBMIT_MIN_WORDS} words to be scored.')

    return text, creator_id, None


# ── Every failure leaves a line ───────────────────────────────────────────────
# A refused request goes through _reject, so the log records it and the caller
# gets a reason. Anything that crashes is caught by _unhandled_error below.

def _reject(http_status: int, reason: str, message: str,
            creator_id: str = "unknown", **extra):
    """Log a refused request, then return the JSON error response for it.

    A related content_id goes in `target_content_id`, never `content_id`. If a
    rejection used `content_id`, entries_for() would see it as that item's
    latest status, and a bad request could change a real item's state.
    """
    audit.log_rejection(creator_id=creator_id, reason=reason,
                        route=request.path, http_status=http_status, **extra)
    body = {"error": reason, "reason": reason, "message": message}
    body.update({k: v for k, v in extra.items() if k == "current_status"})
    return jsonify(body), http_status


@app.errorhandler(Exception)
def _unhandled_error(exc):
    """Any exception a route didn't handle: log it, then answer in JSON.

    The 429 handler further down is more specific, so Flask uses that one for
    rate limits. Other HTTP errors, such as an unknown path (404) or the wrong
    method (405), are logged as rejections. Everything else is a real crash:
    it's logged as an error with an error_id that is also sent to the caller,
    so the response and the log line can be matched up.
    """
    from werkzeug.exceptions import HTTPException

    creator_id = _creator_for_log(_json_object())

    if isinstance(exc, HTTPException):
        try:
            return _reject(exc.code or 500, f"http_{exc.code}", exc.description or exc.name,
                           creator_id=creator_id)
        except Exception:  # noqa: BLE001 - the log itself failed; still answer
            app.logger.exception("Could not write rejection to the audit log")
            return jsonify(error=f"http_{exc.code}", message=exc.description), exc.code

    error_id = f"e_{uuid.uuid4().hex[:12]}"
    # The traceback still goes to the terminal, which is where you debug.
    app.logger.exception("Unhandled error %s on %s", error_id, request.path)

    tb = exc.__traceback__
    while tb is not None and tb.tb_next is not None:
        tb = tb.tb_next
    where = f"{tb.tb_frame.f_code.co_filename.rsplit('/', 1)[-1]}:{tb.tb_lineno}" if tb else "?"

    try:
        audit.log_error(creator_id=creator_id, route=request.path, error_id=error_id,
                        error_type=type(exc).__name__, message=str(exc), where=where)
    except Exception:  # noqa: BLE001 - e.g. disk full; the terminal has it
        app.logger.exception("Could not write error %s to the audit log", error_id)

    return jsonify({
        "error": "internal_error",
        "message": "Something went wrong on our side. Nothing was decided. "
                   "Quote this error_id if you report it.",
        "error_id": error_id,
    }), 500


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        audit.log_rejection(
            creator_id=_creator_for_log(_json_object()),
            reason="rate_limited",
            route=request.path,
            http_status=429,
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.
    ← TODO — Milestones 3, 4 and 5

    Expects JSON:
        {"text": "...", "creator_id": "..."}

    Should return JSON with, at minimum:
        {"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
         "model_score": 0.0, "style_score": 0.0}

    ⚠️ **Both signal scores go in the response, not just the log.** Unit 8's
    `run_attacks.py` and `run_eval.py` read `model_score` and `style_score`
    straight off this response and put them in your reports. Leave them out and
    every row of next unit's evidence says `null` — which is exactly the
    diagnostic you need to name a stage and a mechanism. You do not want to
    find that out after running the attack set.

    ─────────────────────────────────────────────────────────────────────────
    Build it in three passes. Do not skip ahead — the ordering is how you tell
    a broken route from a broken signal.

    **Milestone 3 — the route answers.**
      1. Return a hardcoded response. Confirm `curl` gets it back before you
         add any logic at all.
      2. Then pull `text` and `creator_id` out of the payload.
      3. Then call ONE signal — `detector.model_signal(text)` — and put the
         real number in. Leave confidence and label as placeholders.
      4. Log every submission with `audit.log_decision(...)`. The content_id
         matters: `/appeal` needs it, and a student who skips it rebuilds this
         whole flow later.

    **Milestone 4 — the second signal and the score.**
      5. Add `stylometry.style_signal(text)`.
      6. Combine them with `scoring.combine_signals(...)`.
      7. Log BOTH signal scores alongside the combined one, and put them in the
         response too. Next unit you can't diagnose anything without them.

    **Milestone 5 — the label.**
      8. `scoring.score_to_label(...)` and put the real label in the response.

    ─────────────────────────────────────────────────────────────────────────
    Worth deciding early, because unit 8's attack set will decide it for you:
    what should this do when `text` is missing, empty, or enormous? A crash on
    a malformed input is one of the most common real failures there is.
    """

    # Step 2 - JSON goes in. The whole payload is checked before the signals
    # run, so a malformed body is a 400 with a reason in the log, not a crash.
    payload = _json_object()
    text, creator_id, problem = _validate_submission(payload)
    if problem:
        reason, message = problem
        return _reject(400, reason, message, creator_id=_creator_for_log(payload))

    # Step 3 - one real signal that we first tested from the terminal
    # python detector.py "some text"
    import detector
    import scoring
    import stylometry

    # What model_signal can raise:
    #   ValueError          - under 3 tokens. The minimum-word check makes this
    #                         impossible; the catch is a second line of defence.
    #   DetectorUnavailable - the model can't load. The server's fault, so 503.
    try:
        model_score = detector.model_signal(text)
    except ValueError:
        return _reject(400, "text_too_short", "This text is too short to score.",
                       creator_id=creator_id)
    except detector.DetectorUnavailable:
        return _reject(503, "detector_unavailable",
                       "The checker isn't available right now. Try again later.",
                       creator_id=creator_id)

    # Step 5 - the second signal: python stylometry.py "some text"
    style_score = stylometry.style_signal(text)

    # Step 6 - combine them. The rule is in scoring.py::combine_signals.
    combined_score = scoring.combine_signals(model_score, style_score)

    # Step 8 - turn the score into a guess and the sentence a reader sees.
    guess, label = scoring.score_to_label(combined_score)

    # Step 4 / 7 - log the decision with both signals and the combined score.
    # The content_id is what /appeal needs later.
    content_id = f"c_{uuid.uuid4().hex[:12]}"
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
        status="decided",
    )

    return jsonify({
        "content_id": content_id,
        "creator_id": creator_id,
        "guess": guess,
        "confidence": combined_score,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score,
    }), 200



@app.post("/appeal")
def appeal():
    """
    A writer says you got it wrong. ← TODO — Milestone 5

    Expects JSON:
        {"content_id": "...", "reasoning": "..."}

    Should:
      1. Check the content_id actually exists — `audit.entries_for(id)` tells
         you. A typo here fails silently and looks like a broken endpoint,
         which is the single most common way this milestone eats an hour.
      2. Record the appeal with `audit.log_appeal(...)`, which moves the item
         to `under_review`.
      3. Confirm to the writer. No automatic re-checking needed.

    This is the smallest endpoint in the project and the one that matters most
    to the person on the other end. It's the only thing standing between a
    wrong accusation and nothing at all.
    """
    payload = _json_object()
    if payload is None:
        return _reject(400, "body_not_object",
                       'Send a JSON object like {"content_id": "...", "reasoning": "..."}.')
    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    # Both fields have to be real, non-empty strings. A bad request is logged
    # as a rejection, but no status changes.
    if not isinstance(content_id, str) or not content_id.strip():
        return _reject(400, "invalid_content_id", 'Send JSON with a non-empty "content_id".')
    if not isinstance(reasoning, str) or not reasoning.strip():
        return _reject(400, "invalid_reasoning", 'Send JSON with a non-empty "reasoning".',
                       target_content_id=content_id.strip()[:64])

    # Step 1 - the content_id has to match a decision we actually made, and
    # that decision must still be only "decided": not already appealed, and not
    # already reviewed. A reviewed decision is final; without this check an
    # overturned item could be appealed again and then upheld by a second
    # reviewer. 
    content_id = content_id.strip()
    with audit.locked():
        entries = audit.entries_for(content_id)
        decisions = [e for e in entries if e.get("status") == "decided"]
        if not decisions:
            return _reject(404, "not_found", f"No submission with content_id {content_id[:64]!r}.",
                           target_content_id=content_id[:64])

        original = decisions[-1]
        # Rejections and errors never carry content_id, so the last entry is
        # always a decision, appeal or review: the item's real current status.
        current = entries[-1].get("status")
        if current != "decided":
            message = {
                "under_review": "This decision has already been appealed and is waiting for review.",
                "upheld": "This appeal has already been reviewed, and the original decision was kept.",
                "overturned": "This appeal has already been reviewed, and the decision was overturned.",
            }.get(current if isinstance(current, str) else "",
                  "This decision can't be appealed right now.")
            return _reject(409, "conflict", message,
                           creator_id=original.get("creator_id", "unknown"),
                           target_content_id=content_id, current_status=current)

        # Step 2 - record the appeal beside the original decision. The creator
        # comes from that decision, not the payload, so an appeal can't be filed
        # under someone else's name.
        entry = audit.log_appeal(
            content_id=content_id,
            creator_id=original.get("creator_id"),
            reasoning=reasoning.strip(),
        )

    # Step 3 - confirm to the writer.
    return jsonify({
        "content_id": content_id,
        "status": entry["status"],
        "message": (
            "Thanks, we've received your appeal. A person will review this "
            "decision, and your explanation is saved with it."
        ),
        "original_guess": original.get("guess"),
        "appealed_at": entry["timestamp"],
    }), 200


@app.post("/review")
def review():
    if not config.REVIEWER_TOKEN:
        return _reject(503, "review_disabled", "Reviews are switched off: no REVIEWER_TOKEN is set.")
    # A failed token check is logged without the token that was sent.
    if not hmac.compare_digest(request.headers.get("X-Reviewer-Token", ""), config.REVIEWER_TOKEN):
        return _reject(401, "unauthorized", "Missing or wrong X-Reviewer-Token header.")

    p = _json_object()
    if p is None:
        return _reject(400, "body_not_object",
                       'Send a JSON object with "content_id", "reviewer_id", "outcome" and "note".')

    cid = p.get("content_id")
    reviewer_id = p.get("reviewer_id")
    note = p.get("note")
    outcome = p.get("outcome")
    if (
        not isinstance(cid, str) or not cid.strip()
        or not isinstance(reviewer_id, str) or not reviewer_id.strip()
        or not isinstance(note, str) or not note.strip()
        or outcome not in config.REVIEW_OUTCOMES
    ):
        return _reject(400, "invalid_review",
                       '"content_id", "reviewer_id" and "note" must be non-empty strings, and '
                       f'"outcome" one of {list(config.REVIEW_OUTCOMES)}.')

    cid = cid.strip()
    reviewer_id = reviewer_id.strip()
    note = note.strip()

    with audit.locked():
        entries = audit.entries_for(cid)
        decision = next((e for e in reversed(entries) if e.get("status") == "decided"), None)
        if not decision:
            return _reject(404, "not_found", f"No submission with content_id {cid[:64]!r}.",
                           target_content_id=cid[:64])
        if entries[-1].get("status") != "under_review":
            current = entries[-1].get("status")
            return _reject(409, "conflict", f"Only items under_review can be reviewed; this one is {current!r}.",
                           creator_id=decision.get("creator_id", "unknown"),
                           target_content_id=cid, current_status=current)
        final_guess, final_label = (decision["guess"], decision["label"]) if outcome == "upheld" \
                        else ("human", config.OVERTURNED_LABEL)
        entry = audit.log_review(cid, decision["creator_id"], reviewer_id, outcome, note, final_guess, final_label)

    return jsonify(content_id=cid, status=outcome, original_guess=decision["guess"], final_guess=final_guess, final_label=final_label, reviewed_at=entry["timestamp"]), 200


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
