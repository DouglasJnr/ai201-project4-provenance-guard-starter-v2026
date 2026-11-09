# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 01:39
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_62ade22101b1` | unsure | 0.441 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_165e8696e943` | unsure | 0.463 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_1ee9c959976e` | unsure | 0.557 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_1528a3ee106d` | unsure | 0.591 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_c73c0c001a33` | human | 0.200 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_304f725b0ca8` | unsure | 0.384 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_c48bd5a1512a` | unsure | 0.471 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_d3ef11a09f3a` | unsure | 0.379 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_10562c6e26fc` | unsure | 0.598 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_259feb1e18cd` | ai | 0.883 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_e10eee144492` | unsure | 0.373 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_236ad67f4ae8` | unsure | 0.635 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_90d38b8a33a0` | ai | 0.659 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_4a1c559bc4ce` | ai | 0.774 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_dcafe5000213` | unsure | 0.616 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_3989ed4d1a07` | ai | 0.704 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_778e879869a0` | unsure | 0.634 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_fb99a01f4cf7` | human | 0.215 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_d905d043b4bc` | unsure | 0.368 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_82e5ab7b756b` | human | 0.270 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_07733a6f50a8` | unsure | 0.461 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_08fb43d28ef8` | human | 0.267 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_a355449fa73b` | unsure | 0.430 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_c17e52c19bfa` | unsure | 0.350 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `c_2a96896a6125` | human | 0.150 |  |
| MF04 | malformed | text is only punctuation | 200 | `c_ce3d2f56be9a` | human | 0.250 |  |
| MF05 | malformed | text is a very long single word | 200 | `c_bee9692efb5e` | ai | 0.800 |  |
| MF06 | malformed | text is emoji only | 200 | `c_162ed692481a` | unsure | 0.640 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_40826b82a3fe` | ai | 0.694 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `c_640bee5d83ee` | unsure | 0.640 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `c_4506dbdd50c5` | human | 0.168 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `c_0c07bd5e255f` | human | 0.151 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_16d02469fd6c` | human | 0.234 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_c24ee5d14d6f` | human | 0.234 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_7449c2f6826e` | human | 0.234 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_d88092471d79` | human | 0.234 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_5a4a18e13f9b` | human | 0.234 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_62ade22101b1",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4412,
  "model_score": 0.0176,
  "style_score": 0.8648,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_165e8696e943",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4628,
  "model_score": 0.2946,
  "style_score": 0.631,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_1ee9c959976e",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5567,
  "model_score": 0.4039,
  "style_score": 0.7096,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_1528a3ee106d",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5907,
  "model_score": 0.3184,
  "style_score": 0.8631,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_c73c0c001a33",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.1995,
  "model_score": 0.0667,
  "style_score": 0.3323,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_304f725b0ca8",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.3835,
  "model_score": 0.2666,
  "style_score": 0.5005,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_c48bd5a1512a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4714,
  "model_score": 0.2838,
  "style_score": 0.6589,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_d3ef11a09f3a",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3786,
  "model_score": 0.0382,
  "style_score": 0.719,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_10562c6e26fc",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.598,
  "model_score": 0.4715,
  "style_score": 0.7246,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_259feb1e18cd",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8834,
  "model_score": 0.9895,
  "style_score": 0.7773,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_e10eee144492",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.3732,
  "model_score": 0.3272,
  "style_score": 0.4193,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_236ad67f4ae8",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6352,
  "model_score": 0.5386,
  "style_score": 0.7318,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_90d38b8a33a0",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6593,
  "model_score": 0.6785,
  "style_score": 0.6401,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_4a1c559bc4ce",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7743,
  "model_score": 0.739,
  "style_score": 0.8096,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_dcafe5000213",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6162,
  "model_score": 0.6686,
  "style_score": 0.5639,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_3989ed4d1a07",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7036,
  "model_score": 0.8409,
  "style_score": 0.5663,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_778e879869a0",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6341,
  "model_score": 0.8412,
  "style_score": 0.4271,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_fb99a01f4cf7",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2149,
  "model_score": 0.0672,
  "style_score": 0.3626,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_d905d043b4bc",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.368,
  "model_score": 0.1539,
  "style_score": 0.5821,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_82e5ab7b756b",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2704,
  "model_score": 0.0268,
  "style_score": 0.514,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_07733a6f50a8",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4614,
  "model_score": 0.2946,
  "style_score": 0.6282,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_08fb43d28ef8",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.2667,
  "model_score": 0.1869,
  "style_score": 0.3465,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_a355449fa73b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4298,
  "model_score": 0.3614,
  "style_score": 0.4982,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_c17e52c19bfa",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.3504,
  "model_score": 0.2491,
  "style_score": 0.4518,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_2a96896a6125",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.15,
  "model_score": 0.0,
  "style_score": 0.3,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_ce3d2f56be9a",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2501,
  "model_score": 0.0002,
  "style_score": 0.5,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_bee9692efb5e",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7998,
  "model_score": 0.9996,
  "style_score": 0.6,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_162ed692481a",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9995,
  "style_score": 0.5,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_40826b82a3fe",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.6944,
  "model_score": 0.8888,
  "style_score": 0.5,
  "label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c_640bee5d83ee",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9954,
  "style_score": 0.4499,
  "label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_4506dbdd50c5",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.1682,
  "model_score": 0.0364,
  "style_score": 0.3,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_0c07bd5e255f",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.1511,
  "model_score": 0.0022,
  "style_score": 0.3,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_16d02469fd6c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2338,
  "model_score": 0.0009,
  "style_score": 0.4667,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_c24ee5d14d6f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2338,
  "model_score": 0.0009,
  "style_score": 0.4667,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_7449c2f6826e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2338,
  "model_score": 0.0009,
  "style_score": 0.4667,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_d88092471d79",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2338,
  "model_score": 0.0009,
  "style_score": 0.4667,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_5a4a18e13f9b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2338,
  "model_score": 0.0009,
  "style_score": 0.4667,
  "label": "The text was most likely written by a human as it shows no patterns consistent with those present in AI-generated text.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
