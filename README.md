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

### 1. Flask receives the JSON request containing `text` and `creator_id`.
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

**The rule:** Use an equal-weighted average of the model signal and the style signal. If the two signals disagree by more than 0.40, the result is not allowed to reach the high-confidence AI label: it is capped just below the AI threshold, so a split can produce "unsure" but never "AI". The cap only works in one direction. A low score is left alone, so a split can still produce "human". One signal on its own isn't enough to accuse a writer, because a wrong accusation costs the writer far more than a missed detection costs the site.

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

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
