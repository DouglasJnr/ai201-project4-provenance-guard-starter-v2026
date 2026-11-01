# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False Positive

Given 10 human-written texts, no more than 1 of them may receive the `likely-ai` label.

**Why this target:** A 10% false positive rate is tolerable because wrongly accusing a real writer is more harmful than missing some AI text

---

## 2. Score Spread

At least 4 of 5 clealry AI-written texts must score >= 0.65, and at least 4 of 5 clearly human-written texts must score <= 0.35.

**Why this target:** Thresholds should separate obvious examples by a spread of 0.30 while leaving room for genuinely uncertain writing. The spread means obvious cases should not land close together to show clear separation.

---

## 3. Label Coverage

In a set of 15 texts— 5 clearly human, 5 borderline and 5 clearly AI—the system must return at least 4 human labels, 4 unsure labels and 4 ai labels.

**Why this target:** This verifies that all three labels are reachable and that the system can represent uncertainty instead of forcing every text into one category.


---

## 4. Appeal Path

Every appeal with a valid `content_id` and non-empty reasoning must return HTTP `200`, append an appeal record to the audit log, and mark the submission `under_review`.


**Why this target:** Invalid or or unknown IDs must return 400 or 404 and must not silently change a submission's status.

---

## 5. Bad Input

Out of 5 cases with missing, empty, non-string, whitespace-only `text`, or text under 50 words, and text over 10,000 characters, there must be 0 unhandled cases. The first four must return a 4xx response with a readable message, the short text must return the "uncertain" label with a length warning, and the 100,000-character text must return within 10 seconds, either scored or rejected with a message that states the size limit.


**Why this target:** Both signals are unreliable on very short text (type-token ratio in particular), so the service should say "too little to judge" rather than return a confident verdict from 20 words. The size and timing limit protects the local model from being tied up by one request.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
