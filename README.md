# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

### 1. Flask service receives the JSON request containing `text` and `creator_id`.
### 2. The route extrects the text and creator ID, then checks that the text isn't empty
### 3. The language model, `detector.py` measures how predictable the text is. This then produces `model_score`, where a higher value means the text appears more like AI.
### 4. The style signal, `style.py` measures how the text is structured and written. This produces `style_score`, where a higher value means the text appears more like AI.
### 5. The model score and style score are combined into one overall score from 0.0 to 1.0
### 6. The overall score is converted into a machine-readable guess, and a plain-language label for the reader.
### 7. The service creates a `content_id`, records the creator, both signal scores, the combined score, the guess, and the label in the audit log, then returns those results as JSON to the reader.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity under a local language model. It essentially measures how suprised the model is by each next word, averaged over the text, then converts that to a score between 0 and 1, with a higher score being more AI like.

**Why that might differ between human and AI writing:** Language models generate text by predicting likely next tokens, so its output tends to sit in an area of distribution where another model finds it easy to predict. Human writing on the other hand is less predictable, unusual word choices, sudden changes, and specific details instead of typical ones. AI text tends to be lower perplexity while human text leans to higher perplexity.

**What it can't see:** Whether text is truly human authored as anyone who writes using common words in short, ordinary sentences scores as likely AI. Non-native english speakers will fall into this category as they tend to stick to simpler words that they are more sure of, as well as younger writers and people intentionally writing plainly. 
Text full of uncommon words will likely score as human as well, so formality doesn't decide the score and someone can trick the model.
There is no check whether the text is accurate, coherent, or original. It only checks how likely the word sequence is.

### Signal two — the style signal

**What it measures:** The statistical shape of the text without any understanding of any of it. Five measures, each mapped onto a 0–1 "AI-ness" scale between two anchor values and then combined by weight:

| Measure | What it is | Maps to 1.0 (AI-like) | Maps to 0.0 (human-like) | Weight |
|---|---|---|---|---|
| Sentence length spread | std dev of sentence length ÷ mean | 0.2 or less | 1.0 or more | 0.30 |
| Abstract vocabulary | share of words that are 9+ letters, or 7+ letters ending in -tion, -ment, -ity, -ness… | 0.20 or more | 0 | 0.30 |
| Transition words | "first", "finally", "additionally", "moreover"… per word | 0.05 or more | 0 | 0.15 |
| Punctuation density | commas, semicolons, colons, dashes, brackets, quotes, ! and ? per word (full stops and apostrophes not counted) | 0 | 0.10 or more | 0.15 |
| Type-token ratio | unique words ÷ total words | 0.65 or less | 0.95 or more | 0.10 |

Rhythm (spread + punctuation) and word choice (abstract + transitions) get 0.45 each. Type-token ratio gets only 0.10 because it falls as text gets longer, so across inputs of different lengths it measures length as much as vocabulary. A one-sentence text has no spread to measure, so that measure sits at a neutral 0.5; empty text scores 0.5 overall.

**Why that might differ between human and AI writing:** AI text leans towards even, mid-length sentences and less varied band of vocabulary. Human writing is less structured, a four word sentence can be next to a thirty-word sentence, with more varied punctuation and broader vocabulary. AI explainer prose also leans on long abstract nouns ("prioritization", "environment") and listing scaffolding ("First… Second… Finally…"), where plain human writing uses short concrete words ("bus", "shelves").

**Why the last two measures were added:** With only the first three, plain conventional human writing scored 0.86 on this signal, higher than the clearly-AI sample (0.63). Its sentences are even and it has almost no punctuation, so on rhythm alone it looks machine-made, and signal one rates it as AI-like too. Adding word-choice measures brought it down to 0.48.

**What it can't see:** It can't see the content. It is easily manipulated as any change of the text shape without any change to the substance of the text affects the score. Adding typos, varying punctuation, chopping up sentences and pasting quotations will deceive it. The two word-choice measures add their own blind spots: formal and academic human writing uses long abstract words and scores as more AI-like, writers taught the five-paragraph essay use transition words just as AI does, and deleting the transition words takes seconds. Short texts are noisy: in "One sentence only." a single -ence word makes a third of the text count as abstract. The anchor values were tuned on four calibration texts, so they are a starting point, not a measured result.

### The combining rule

**The rule:** `scoring.py::combine_signals` Use an equal-weighted average of the model signal and the style signal. If the two signals disagree by more than 0.40, the result is not allowed to reach the high-confidence AI label: it is capped just below the AI threshold, so a split can produce "unsure" but never "AI". The cap only works in one direction. A low score is left alone, so a split can still produce "human". One signal on its own isn't enough to accuse a writer, because a wrong accusation costs the writer far more than a missed detection costs the site.

**The numbers:**

- `combined_score` = (0.5 × `model_score`) + (0.5 × `style_score`)
- if |`model_score` − `style_score`| > 0.40: `combined_score` = min(`combined_score`, `AI_THRESHOLD` − 0.01) = min(`combined_score`, 0.64)
- `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5` and `DISAGREEMENT_GAP = 0.40` live in `config.py`.

**Why the cap sits 0.01 below the threshold:** So the cap holds whether `score_to_label` compares with `>` or `>=`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A model signal of 0.95 with a style signal of 0.45: text the language model finds very predictable, but with uneven sentences and concrete vocabulary. That's what AI text looks like after someone chops up its sentences, and also what very plain human writing with some variety looks like. The plain average is 0.70, which would be labelled AI. The signals differ by 0.50, more than the 0.40 gap, so the rule caps the score at 0.64 and the label is "unsure". The writer isn't accused on the strength of one signal.

The opposite split behaves differently on purpose. A model signal of 0.05 with a style signal of 0.60 averages to 0.33, and the cap leaves it alone, so the label is "human".

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text. |
| unsure | >0.35 and <0.65 | It is unclear whether this was written by a human or AI.Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything  |
| high-confidence AI | 0.65 - 1.00 | The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain,simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.|

**Why I worded the "unsure" one this way:**

The person reading "unsure" may well have written every word themselves. So the label plainly says that we don't know. It explains why without blaming the writer: plain, clear writing is a known reason for this result, not a sign of cheating. And it says outright that this is not a finding of AI use and that nothing is required of them. I left out the word "suspected" and any request for them to prove anything, because a label that asks an innocent writer to defend themselves is an accusation in softer words.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I started working at the library last spring. Most of my job is putting books back on the shelves and helping people find things. It is not hard work but it can get busy in the afternoon when the school lets out. I like the people I work with and the hours fit around my classes. I plan to stay there until I graduate.", "creator_id": "jr_writer"}'
```

```json
{
  "combined_score": 0.5987,
  "confidence": 0.5987,
  "content_id": "c_67101e53114c",
  "creator_id": "jr",
  "guess": "unsure",
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "model_score": 0.7223,
  "style_score": 0.475
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5050/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_67101e53114c", "reasoning": "I wrote this myself. It is about my own job at the library, and I kept the sentences simple on purpose."}'
```

```json
{
  "appealed_at": "2026-11-02T07:28:30+00:00",
  "content_id": "c_67101e53114c",
  "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
  "original_guess": "unsure",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5050/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.5987,
      "content_id": "c_67101e53114c",
      "creator_id": "jr",
      "guess": "unsure",
      "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "model_score": 0.7223,
      "status": "decided",
      "style_score": 0.475,
      "timestamp": "2026-11-02T07:27:43+00:00"
    },
    {
      "content_id": "c_67101e53114c",
      "creator_id": "jr",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is about my own job at the library, and I kept the sentences simple on purpose.",
      "status": "under_review",
      "timestamp": "2026-11-02T07:28:30+00:00"
    }
  ]
}
```

The original decision is left exactly as it was; the appeal is a second entry beside it with the same `content_id`. The log is append-only, so it shows what was decided, that it was challenged, and in what order. An appeal with a missing or empty `content_id` or `reasoning` returns 400, and an unknown `content_id` returns 404; neither writes anything to the log or changes any status.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I asked Claude to help me brainstorm how to modify my signals to handle the blindspot for plain, simple human-text being mislabelled.
- *What came back:* Suggestion to add abstract vocabulary and transition rate to `style_signal` as it is the easier signal to deceive.
- *What I changed:* Modified my `stylometry.py` file to add calculations for the above mentioned measurements an dadded them to my style_score calculation.

**Moment 2**

- *What I asked for:* generate code for the /appeal endpoint
- *What came back:* working code, that was missing the check for empty `content_id`
- *What I changed:* Added the necessary checks for empty or whitespaces in `content_id` where a `400` error should be returned.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** _5__ per minute, __100_ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->
     The 5 per minute stops bursts, probing, and sudden compute spikes while allowing a real writer to resubmit corrections to their work. The 100 per day acts as a slow window to control cumulative resource usage without limiting short activity. The combination catches burst and sustained abuse.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
{"timestamp": "2026-11-05T02:30:40+00:00", "content_id": "c_a8183384c2b8", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.3323, "combined_score": 0.3267, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:40+00:00", "content_id": "c_0b2a1af5277c", "creator_id": "attacker_FP01", "guess": "unsure", "model_score": 0.6175, "style_score": 0.4193, "combined_score": 0.5184, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:41+00:00", "content_id": "c_43dcc32e959a", "creator_id": "attacker_FP02", "guess": "ai", "model_score": 0.7387, "style_score": 0.7318, "combined_score": 0.7352, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:41+00:00", "content_id": "c_7333586bc4a8", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6401, "combined_score": 0.7226, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:41+00:00", "content_id": "c_203a2bbd64b1", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.8096, "combined_score": 0.8213, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:41+00:00", "content_id": "c_114d5e0e1ea5", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.5639, "combined_score": 0.6822, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:41+00:00", "content_id": "c_5faecf67e606", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8814, "style_score": 0.5663, "combined_score": 0.7238, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:41+00:00", "content_id": "c_3855412c0594", "creator_id": "attacker_FP07", "guess": "unsure", "model_score": 0.8816, "style_score": 0.4271, "combined_score": 0.64, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:42+00:00", "content_id": "c_1324e81401f0", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.3, "combined_score": 0.15, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:42+00:00", "content_id": "c_08c1f3c752a4", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0112, "style_score": 0.5, "combined_score": 0.2556, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:42+00:00", "content_id": "c_25dbc879352b", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6, "combined_score": 0.7988, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:43+00:00", "content_id": "c_b8601c54763c", "creator_id": {"id": "x"}, "guess": "human", "model_score": 0.0492, "style_score": 0.3, "combined_score": 0.1746, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-05T02:30:43+00:00", "creator_id": "attacker_RQ12", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it: 
`FP03` because it classified a non-native english speaker's careful writing as AI with a score 0f 0.723. It is harmful because the sustem is mistaking straightforward, carefully chosen English for machine-generated writing. It unfairly penalizes someone for their language background rather than detecting actual AI use.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Own writing flagged as AI | <=1 of 10 | 0 / 10  | 0 / 10 | 0 / 10  | MET |
| 2. Score spread | ≥ 4 / 5 clearly-AI score ≥ 0.65 **and** ≥ 4 / 5 clearly-human score ≤ 0.35 | 6 / 10 | 6 / 10 | 6 / 10 | MISSED |
| 3. Label coverage | ≥ 4 each of `human`, `unsure`, `ai` | 2 human · 7 unsure · 6 ai | 2 human · 7 unsure · 6 ai | 2 human · 7 unsure · 6 ai | MISSED |
| 4. Appeal path always changes status| 6 / 6 | 6 / 6 | 6 / 6 | 6 / 6 | MET |
| 5. Handled Bad input cases | 7 / 7 | 5 / 7 | 5 / 7 | 5 / 7 | MISSED |

All three trials returned identical scores for every input, so no result
changed from trial to trial. Source: `results/run_2026-11-08_2028_before.md`.

Criterion 4 isn't covered by `run_eval.py`, which only posts to `/submit`. I
tested it with `run_appeals.py` against the running service (2026-11-08
22:14), three trials. Each trial submitted two fresh texts, appealed the first
one properly, then sent five bad appeals (unknown id, missing id, empty id,
missing reasoning, whitespace-only reasoning) aimed at the second. After every
request I checked the new lines in `logs/audit.jsonl` and the second
submission's status. Raw output: `results/appeal_run_2026-11-08.json`.



**Real output from one trial**, pasted as text, naming the file and function
that produced it — `run_eval.py::main` posting to `app.py::submit`, criterion 3
trial 1, text 5 (a clearly-human text labelled AI):

My own writing, trial 1 `run_eval.py::main` posting to `app.py::submit`:
```json
{
  "status": 200,
  "guess": "ai",
  "confidence": 0.6549,
  "model_score": 0.7674,
  "style_score": 0.5424,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "sent": "For the next month I found myself attend"
}
```

Score spread, trial 1 `run_eval.py::main` posting to `app.py::submit`:
```json
{
    "status": 200,
    "guess": "human",
    "confidence": 0.3473,
    "model_score": 0.2992,
    "style_score": 0.3954,
    "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
    "sent": "An hour until kick-off, the announcement of the team line-ups saw the "
  },
```

label coverage, trial 1 `run_eval.py::main` posting to `app.py::submit`:
```json
{
    "status": 200,
    "guess": "human",
    "confidence": 0.3415,
    "model_score": 0.2492,
    "style_score": 0.4338,
    "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
    "sent": " I initially began as the introverted and reserved version of myself, "
  },
```

Valid appeal, trial 1 — response from `app.py::appeal`:

```json
{
  "appealed_at": "2026-11-09T03:14:35+00:00",
  "content_id": "c_89eafb9eeb70",
  "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
  "original_guess": "human",
  "status": "under_review"
}
```

and the line it appended to `logs/audit.jsonl` via `audit.py::log_appeal`:

```json
{"timestamp": "2026-11-09T03:14:35+00:00", "content_id": "c_89eafb9eeb70", "creator_id": "eval_appeal_t1_a", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself about my own week."}
```

Unknown id, trial 1 — HTTP 404, nothing logged:

```json
{
  "error": "not_found",
  "message": "No submission with content_id 'c_doesnotexist'."
}
```

Bad Input, trial 1 `run_eval.py::main` posting to `app.py::submit`:
```json
{
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_nonstring\"}"
  },
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->


**1. Plain and formal human writing labelled AI — signal one and combining rule** Covers criterion 2 (human side 1 / 5), criterion 3 (only 2 `human` labels out of expected 5), and FP01–FP07. `detector.py::model_signal` turns low perplexity into a high AI score, and GPT-2 finds plain, formal, rubric-shaped, technical and careful non-native English predictable: FP01–FP07 scored 0.62–0.88 on signal one. Signal two
doesn't pull them back, because `stylometry.py::style_signal` rewards the same
things formal writing has: abstract nouns, transition words, even sentence
lengths. FP02 (0.73) and FP04 (0.81) scored AI on both. The combining rule's
safety net, `scoring.py::combine_signals` capping the score when the signals
differ by more than 0.40, fires only on FP07 (gap 0.45), which is why FP07
stopped at 0.64 `unsure`. Everywhere else the gaps were 0.01–0.32 (FP03 0.17,
criterion 3 text 5 0.23), so the cap never applied. On the criterion 2 and 3 human texts that missed, both signals sit in the middle: model 0.34–0.77,
style 0.42–0.56. The average of two middling scores lands in `unsure`, and
`human` needs it below 0.35, so the human label is only reachable when both
signals are low. 

**2. The route accepts text that isn't really text — the route.** Covers the
criterion 5 short-text case and MF02–MF05. `app.py::submit` only checks that
`text` is a non-empty string. It has no minimum length and no check that the
text contains words.

**3. Malformed request bodies aren't validated — the route.** Covers RQ07 and
RQ06. `app.py::submit` does `request.get_json(silent=True) or {}`. A JSON
array is truthy, so it gets through, and `.get` on a list raises
`AttributeError`, giving a 500 (**RQ07**). `creator_id` is never type-checked,
so an object was accepted and written into the audit log as
`{"id": "x"}` (**RQ06**).

**4. No size limit — the route, and signal one's token window.** Covers MF08
and the criterion 5 huge-text case. The route accepts any length. Signal one
truncates to `DETECTOR_MAX_TOKENS` (400), so only the first ~300 words are
judged. MF08 (60,000 characters) and the 250,000-character criterion 5 body
both hit the disagreement cap at 0.64 (model 0.99, style 0.40–0.45) instead
of being rejected with a size-limit message. The criterion's 10-second limit
also wasn't measured, which is a gap in the test, not a mechanism.

---

## The Improvement

**What I changed:** Changed the midpoint and steepness values of my model signal

**Which diagnosis pointed at it:** Diagnosis 1. Essays with a perplexity score of 31-45 were being labelled AI.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->
```json
 {"c_62ade22101b1", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.0176, "style_score": 0.8648, "combined_score": 0.4412, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:55+00:00", "content_id": "c_165e8696e943", "creator_id": "attacker_EV02", "guess": "unsure", "model_score": 0.2946, "style_score": 0.631, "combined_score": 0.4628, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:55+00:00", "content_id": "c_1ee9c959976e", "creator_id": "attacker_EV03", "guess": "unsure", "model_score": 0.4039, "style_score": 0.7096, "combined_score": 0.5567, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:55+00:00", "content_id": "c_1528a3ee106d", "creator_id": "attacker_EV04", "guess": "unsure", "model_score": 0.3184, "style_score": 0.8631, "combined_score": 0.5907, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:55+00:00", "content_id": "c_c73c0c001a33", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.0667, "style_score": 0.3323, "combined_score": 0.1995, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:56+00:00", "content_id": "c_304f725b0ca8", "creator_id": "attacker_EV06", "guess": "unsure", "model_score": 0.2666, "style_score": 0.5005, "combined_score": 0.3835, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:56+00:00", "content_id": "c_c48bd5a1512a", "creator_id": "attacker_EV07", "guess": "unsure", "model_score": 0.2838, "style_score": 0.6589, "combined_score": 0.4714, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:56+00:00", "content_id": "c_d3ef11a09f3a", "creator_id": "attacker_EV08", "guess": "unsure", "model_score": 0.0382, "style_score": 0.719, "combined_score": 0.3786, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:56+00:00", "content_id": "c_10562c6e26fc", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.4715, "style_score": 0.7246, "combined_score": 0.598, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:56+00:00", "content_id": "c_259feb1e18cd", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9895, "style_score": 0.7773, "combined_score": 0.8834, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:57+00:00", "content_id": "c_e10eee144492", "creator_id": "attacker_FP01", "guess": "unsure", "model_score": 0.3272, "style_score": 0.4193, "combined_score": 0.3732, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:57+00:00", "content_id": "c_236ad67f4ae8", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.5386, "style_score": 0.7318, "combined_score": 0.6352, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:57+00:00", "content_id": "c_90d38b8a33a0", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.6785, "style_score": 0.6401, "combined_score": 0.6593, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:57+00:00", "content_id": "c_4a1c559bc4ce", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.739, "style_score": 0.8096, "combined_score": 0.7743, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:57+00:00", "content_id": "c_dcafe5000213", "creator_id": "attacker_FP05", "guess": "unsure", "model_score": 0.6686, "style_score": 0.5639, "combined_score": 0.6162, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:58+00:00", "content_id": "c_3989ed4d1a07", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8409, "style_score": 0.5663, "combined_score": 0.7036, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:58+00:00", "content_id": "c_778e879869a0", "creator_id": "attacker_FP07", "guess": "unsure", "model_score": 0.8412, "style_score": 0.4271, "combined_score": 0.6341, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:58+00:00", "content_id": "c_fb99a01f4cf7", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.0672, "style_score": 0.3626, "combined_score": 0.2149, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:58+00:00", "content_id": "c_d905d043b4bc", "creator_id": "attacker_PI01", "guess": "unsure", "model_score": 0.1539, "style_score": 0.5821, "combined_score": 0.368, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:58+00:00", "content_id": "c_82e5ab7b756b", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.0268, "style_score": 0.514, "combined_score": 0.2704, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:58+00:00", "content_id": "c_07733a6f50a8", "creator_id": "attacker_PI03", "guess": "unsure", "model_score": 0.2946, "style_score": 0.6282, "combined_score": 0.4614, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:59+00:00", "content_id": "c_08fb43d28ef8", "creator_id": "attacker_PI04", "guess": "human", "model_score": 0.1869, "style_score": 0.3465, "combined_score": 0.2667, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:59+00:00", "content_id": "c_a355449fa73b", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.3614, "style_score": 0.4982, "combined_score": 0.4298, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:59+00:00", "content_id": "c_c17e52c19bfa", "creator_id": "attacker_PI06", "guess": "unsure", "model_score": 0.2491, "style_score": 0.4518, "combined_score": 0.3504, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:59+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:38:59+00:00", "content_id": "c_2a96896a6125", "creator_id": "attacker_MF03", "guess": "human", "model_score": 0.0, "style_score": 0.3, "combined_score": 0.15, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:38:59+00:00", "content_id": "c_ce3d2f56be9a", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0002, "style_score": 0.5, "combined_score": 0.2501, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:00+00:00", "content_id": "c_bee9692efb5e", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9996, "style_score": 0.6, "combined_score": 0.7998, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:01+00:00", "content_id": "c_162ed692481a", "creator_id": "attacker_MF06", "guess": "unsure", "model_score": 0.9995, "style_score": 0.5, "combined_score": 0.64, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:01+00:00", "content_id": "c_40826b82a3fe", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.8888, "style_score": 0.5, "combined_score": 0.6944, "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_640bee5d83ee", "creator_id": "attacker_MF08", "guess": "unsure", "model_score": 0.9954, "style_score": 0.4499, "combined_score": 0.64, "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_RQ01", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_4506dbdd50c5", "creator_id": "unknown", "guess": "human", "model_score": 0.0364, "style_score": 0.3, "combined_score": 0.1682, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_RQ03", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_RQ04", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_RQ05", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_0c07bd5e255f", "creator_id": {"id": "x"}, "guess": "human", "model_score": 0.0022, "style_score": 0.3, "combined_score": 0.1511, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_RQ12", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_16d02469fd6c", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0009, "style_score": 0.4667, "combined_score": 0.2338, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_c24ee5d14d6f", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0009, "style_score": 0.4667, "combined_score": 0.2338, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_7449c2f6826e", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0009, "style_score": 0.4667, "combined_score": 0.2338, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_d88092471d79", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0009, "style_score": 0.4667, "combined_score": 0.2338, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "content_id": "c_5a4a18e13f9b", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0009, "style_score": 0.4667, "combined_score": 0.2338, "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.", "status": "decided"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-09T06:39:02+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
```


**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, the improvement did help with diagnosis 1. Fewer human writers are accused: FP labelled `ai` went from 5 to 3, human texts in my criteria now reach `human`, and criterion 3 passes written. No extra edited AI text got labelled `human`. The trade off is that the system is less confident on AI text.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->
The system still misses criterion 2,3, and 5. FP attacks still get through, and the system is less confident about AI text now. Next I would only allow `ai` labels when the style signal is at least 0.70, and validate in the route for text length or text with no letters. I had to stop because we only eeded 1 improvement and I did not have more time to implement any further changes to the system.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->
     I would keep the lower midpoint and accept that more AI text lands in `unsure` instead of `ai`. I would rather less AI text be caught than non-native and formal writers get accused of using AI as that is that is a more expensive mistake.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
