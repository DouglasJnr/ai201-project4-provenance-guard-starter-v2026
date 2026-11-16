# Review run — before

- Produced by: `run_reviews.py` · scenarios: `scenarios.py::REVIEW_SCENARIOS`
- Service: `app.py::review`, `app.py::appeal` (in-process, Flask test client)
- Log for this run: `logs/review_eval_2026-11-15_1914.jsonl`
- 3 trials per criterion · 2026-11-15 19:16

Each cell is how many cases did what scenarios.py expected. Fill in
Target from `criteria.md` and the Verdict yourself.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 6. a review resolves an appeal |  | 5/5 | 5/5 | 5/5 |  |
| 7. only a reviewer can review |  | 5/5 | 5/5 | 5/5 |  |
| 8. a reviewed decision is final, and bad review requests change nothing |  | 8/10 | 8/10 | 8/10 |  |
| 9. two reviews at the same moment |  | 5/5 | 5/5 | 5/5 |  |
| 10. crashes are still traceable |  | 5/5 | 5/5 | 5/5 |  |

---

## Cases that didn't do what was expected

| Criterion | Trial | Case | Expected | Got |
|---|---|---|---|---|
| 8 | 1 | appeal an under_review item again | 409 | 200 |
| 8 | 1 | appeal an already reviewed item | 409 | 200 |
| 8 | 2 | appeal an under_review item again | 409 | 200 |
| 8 | 2 | appeal an already reviewed item | 409 | 200 |
| 8 | 3 | appeal an under_review item again | 409 | 200 |
| 8 | 3 | appeal an already reviewed item | 409 | 200 |

---

## What actually came back

Real output, token redacted. The full log lines are in the log above.

### 6. a review resolves an appeal

**Trial 1**

```json
[
  {
    "case": "overturned (text 1)",
    "content_id": "c_d529c910455b",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_d529c910455b",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:09+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "upheld (text 1)",
    "content_id": "c_85c5dfea33c7",
    "expect": "200, final_guess=ai",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "ai",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_85c5dfea33c7",
      "final_guess": "ai",
      "final_label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:12+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "upheld (text 2)",
    "content_id": "c_71c852979074",
    "expect": "200, final_guess=unsure",
    "http": 200,
    "original_guess": "unsure",
    "final_guess": "unsure",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_71c852979074",
      "final_guess": "unsure",
      "final_label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "original_guess": "unsure",
      "reviewed_at": "2026-11-16T00:15:14+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "overturned (text 3)",
    "content_id": "c_86886c61db58",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "human",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_86886c61db58",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "human",
      "reviewed_at": "2026-11-16T00:15:14+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "overturned (text 1)",
    "content_id": "c_218117394a28",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_218117394a28",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:14+00:00",
      "status": "overturned"
    }
  }
]
```

**Trial 2**

```json
[
  {
    "case": "overturned (text 1)",
    "content_id": "c_01b03aacaf42",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_01b03aacaf42",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:14+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "upheld (text 1)",
    "content_id": "c_8d46f97b4105",
    "expect": "200, final_guess=ai",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "ai",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_8d46f97b4105",
      "final_guess": "ai",
      "final_label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:14+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "upheld (text 2)",
    "content_id": "c_947db2c579d0",
    "expect": "200, final_guess=unsure",
    "http": 200,
    "original_guess": "unsure",
    "final_guess": "unsure",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_947db2c579d0",
      "final_guess": "unsure",
      "final_label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "original_guess": "unsure",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "overturned (text 3)",
    "content_id": "c_0c937f73154c",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "human",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_0c937f73154c",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "human",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "overturned (text 1)",
    "content_id": "c_85af7fd4807f",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_85af7fd4807f",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "overturned"
    }
  }
]
```

**Trial 3**

```json
[
  {
    "case": "overturned (text 1)",
    "content_id": "c_c4bb66786630",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_c4bb66786630",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "upheld (text 1)",
    "content_id": "c_3da846c6a43b",
    "expect": "200, final_guess=ai",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "ai",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_3da846c6a43b",
      "final_guess": "ai",
      "final_label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "upheld (text 2)",
    "content_id": "c_f8bcda526443",
    "expect": "200, final_guess=unsure",
    "http": 200,
    "original_guess": "unsure",
    "final_guess": "unsure",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_f8bcda526443",
      "final_guess": "unsure",
      "final_label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "original_guess": "unsure",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "overturned (text 3)",
    "content_id": "c_458ad867a8ce",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "human",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_458ad867a8ce",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "human",
      "reviewed_at": "2026-11-16T00:15:15+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "overturned (text 1)",
    "content_id": "c_ea6bd708dfa4",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_ea6bd708dfa4",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T00:15:16+00:00",
      "status": "overturned"
    }
  }
]
```

### 7. only a reviewer can review

**Trial 1**

```json
[
  {
    "case": "no header",
    "content_id": "c_c0de2b01f802",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "empty token",
    "content_id": "c_d0ddee589876",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "made-up token",
    "content_id": "c_30ba69668789",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "real token + 1 character",
    "content_id": "c_b303221a5e1d",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "real token, wrong header",
    "content_id": "c_35d3a56e51ce",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  }
]
```

**Trial 2**

```json
[
  {
    "case": "no header",
    "content_id": "c_2d9a77835aac",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "empty token",
    "content_id": "c_5269ca8262ef",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "made-up token",
    "content_id": "c_d9f551ccd37d",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "real token + 1 character",
    "content_id": "c_c5e29a6ff0b0",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "real token, wrong header",
    "content_id": "c_60b7a6325ac1",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  }
]
```

**Trial 3**

```json
[
  {
    "case": "no header",
    "content_id": "c_5478ff6e477f",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "empty token",
    "content_id": "c_1068711c8ca0",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "made-up token",
    "content_id": "c_8b03075b4a55",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "real token + 1 character",
    "content_id": "c_1cc035e1007c",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  },
  {
    "case": "real token, wrong header",
    "content_id": "c_ce1b37ba103a",
    "expect": 401,
    "http": 401,
    "status_before": "under_review",
    "status_after": "under_review",
    "review_lines": 0,
    "unauthorized_lines": 1,
    "token_in_log": false,
    "as_expected": true,
    "response": {
      "error": "unauthorized",
      "message": "Missing or wrong X-Reviewer-Token header.",
      "reason": "unauthorized"
    }
  }
]
```

### 8. a reviewed decision is final, and bad review requests change nothing

**Trial 1**

```json
[
  {
    "case": "body is a JSON array",
    "route": "/review",
    "content_id": "c_0882ddef1501",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "body_not_object",
      "message": "Send a JSON object with \"content_id\", \"reviewer_id\", \"outcome\" and \"note\".",
      "reason": "body_not_object"
    }
  },
  {
    "case": "outcome missing",
    "route": "/review",
    "content_id": "c_7908a06077ba",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "outcome not allowed",
    "route": "/review",
    "content_id": "c_4da526d0f2ca",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "whitespace note",
    "route": "/review",
    "content_id": "c_4ad798be8e3f",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "reviewer_id not a string",
    "route": "/review",
    "content_id": "c_6dcc016d043e",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "unknown content_id",
    "route": "/review",
    "content_id": "c_f27ed960fa31",
    "expect": 404,
    "http": 404,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id 'c_doesnotexist'.",
      "reason": "not_found"
    }
  },
  {
    "case": "never appealed",
    "route": "/review",
    "content_id": "c_2f91edec2642",
    "expect": 409,
    "http": 409,
    "status_before": "decided",
    "status_after": "decided",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "decided",
      "error": "conflict",
      "message": "Only items under_review can be reviewed; this one is 'decided'.",
      "reason": "conflict"
    }
  },
  {
    "case": "second review of a reviewed item",
    "route": "/review",
    "content_id": "c_10875564bfea",
    "expect": 409,
    "http": 409,
    "status_before": "overturned",
    "status_after": "overturned",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "overturned",
      "error": "conflict",
      "message": "Only items under_review can be reviewed; this one is 'overturned'.",
      "reason": "conflict"
    }
  },
  {
    "case": "appeal an under_review item again",
    "route": "/appeal",
    "content_id": "c_7838b4b04ebd",
    "expect": 409,
    "http": 200,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 1,
    "rejected_lines": 0,
    "as_expected": false,
    "response": {
      "appealed_at": "2026-11-16T00:15:47+00:00",
      "content_id": "c_7838b4b04ebd",
      "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
      "original_guess": "ai",
      "status": "under_review"
    }
  },
  {
    "case": "appeal an already reviewed item",
    "route": "/appeal",
    "content_id": "c_c9e9d3f15bfa",
    "expect": 409,
    "http": 200,
    "status_before": "overturned",
    "status_after": "under_review",
    "item_lines_added": 1,
    "rejected_lines": 0,
    "as_expected": false,
    "response": {
      "appealed_at": "2026-11-16T00:15:51+00:00",
      "content_id": "c_c9e9d3f15bfa",
      "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
      "original_guess": "ai",
      "status": "under_review"
    }
  }
]
```

**Trial 2**

```json
[
  {
    "case": "body is a JSON array",
    "route": "/review",
    "content_id": "c_4f197d1a1498",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "body_not_object",
      "message": "Send a JSON object with \"content_id\", \"reviewer_id\", \"outcome\" and \"note\".",
      "reason": "body_not_object"
    }
  },
  {
    "case": "outcome missing",
    "route": "/review",
    "content_id": "c_c15ffb53b516",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "outcome not allowed",
    "route": "/review",
    "content_id": "c_a2c081db9308",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "whitespace note",
    "route": "/review",
    "content_id": "c_591c1759f0a7",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "reviewer_id not a string",
    "route": "/review",
    "content_id": "c_4b8dd428b172",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "unknown content_id",
    "route": "/review",
    "content_id": "c_e2fb56cf373d",
    "expect": 404,
    "http": 404,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id 'c_doesnotexist'.",
      "reason": "not_found"
    }
  },
  {
    "case": "never appealed",
    "route": "/review",
    "content_id": "c_5b64f56f73e9",
    "expect": 409,
    "http": 409,
    "status_before": "decided",
    "status_after": "decided",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "decided",
      "error": "conflict",
      "message": "Only items under_review can be reviewed; this one is 'decided'.",
      "reason": "conflict"
    }
  },
  {
    "case": "second review of a reviewed item",
    "route": "/review",
    "content_id": "c_6d5052109a99",
    "expect": 409,
    "http": 409,
    "status_before": "overturned",
    "status_after": "overturned",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "overturned",
      "error": "conflict",
      "message": "Only items under_review can be reviewed; this one is 'overturned'.",
      "reason": "conflict"
    }
  },
  {
    "case": "appeal an under_review item again",
    "route": "/appeal",
    "content_id": "c_daafef1a0a48",
    "expect": 409,
    "http": 200,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 1,
    "rejected_lines": 0,
    "as_expected": false,
    "response": {
      "appealed_at": "2026-11-16T00:16:09+00:00",
      "content_id": "c_daafef1a0a48",
      "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
      "original_guess": "ai",
      "status": "under_review"
    }
  },
  {
    "case": "appeal an already reviewed item",
    "route": "/appeal",
    "content_id": "c_069786b82fa9",
    "expect": 409,
    "http": 200,
    "status_before": "overturned",
    "status_after": "under_review",
    "item_lines_added": 1,
    "rejected_lines": 0,
    "as_expected": false,
    "response": {
      "appealed_at": "2026-11-16T00:16:12+00:00",
      "content_id": "c_069786b82fa9",
      "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
      "original_guess": "ai",
      "status": "under_review"
    }
  }
]
```

**Trial 3**

```json
[
  {
    "case": "body is a JSON array",
    "route": "/review",
    "content_id": "c_47730e32658f",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "body_not_object",
      "message": "Send a JSON object with \"content_id\", \"reviewer_id\", \"outcome\" and \"note\".",
      "reason": "body_not_object"
    }
  },
  {
    "case": "outcome missing",
    "route": "/review",
    "content_id": "c_31db3bc947c6",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "outcome not allowed",
    "route": "/review",
    "content_id": "c_a5530b929eb9",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "whitespace note",
    "route": "/review",
    "content_id": "c_f255a7e311fc",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "reviewer_id not a string",
    "route": "/review",
    "content_id": "c_c38898039dc2",
    "expect": 400,
    "http": 400,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "invalid_review",
      "message": "\"content_id\", \"reviewer_id\" and \"note\" must be non-empty strings, and \"outcome\" one of ['upheld', 'overturned'].",
      "reason": "invalid_review"
    }
  },
  {
    "case": "unknown content_id",
    "route": "/review",
    "content_id": "c_13df71bcfef2",
    "expect": 404,
    "http": 404,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id 'c_doesnotexist'.",
      "reason": "not_found"
    }
  },
  {
    "case": "never appealed",
    "route": "/review",
    "content_id": "c_c0911e5b242a",
    "expect": 409,
    "http": 409,
    "status_before": "decided",
    "status_after": "decided",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "decided",
      "error": "conflict",
      "message": "Only items under_review can be reviewed; this one is 'decided'.",
      "reason": "conflict"
    }
  },
  {
    "case": "second review of a reviewed item",
    "route": "/review",
    "content_id": "c_0d8d0bb30961",
    "expect": 409,
    "http": 409,
    "status_before": "overturned",
    "status_after": "overturned",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "overturned",
      "error": "conflict",
      "message": "Only items under_review can be reviewed; this one is 'overturned'.",
      "reason": "conflict"
    }
  },
  {
    "case": "appeal an under_review item again",
    "route": "/appeal",
    "content_id": "c_52b5810549cc",
    "expect": 409,
    "http": 200,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 1,
    "rejected_lines": 0,
    "as_expected": false,
    "response": {
      "appealed_at": "2026-11-16T00:16:14+00:00",
      "content_id": "c_52b5810549cc",
      "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
      "original_guess": "ai",
      "status": "under_review"
    }
  },
  {
    "case": "appeal an already reviewed item",
    "route": "/appeal",
    "content_id": "c_10435dbc0ee9",
    "expect": 409,
    "http": 200,
    "status_before": "overturned",
    "status_after": "under_review",
    "item_lines_added": 1,
    "rejected_lines": 0,
    "as_expected": false,
    "response": {
      "appealed_at": "2026-11-16T00:16:14+00:00",
      "content_id": "c_10435dbc0ee9",
      "message": "Thanks, we've received your appeal. A person will review this decision, and your explanation is saved with it.",
      "original_guess": "ai",
      "status": "under_review"
    }
  }
]
```

### 9. two reviews at the same moment

**Trial 1**

```json
[
  {
    "case": "run 1",
    "content_id": "c_d0ae4c1f7658",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 2",
    "content_id": "c_9144f34012ca",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 3",
    "content_id": "c_98965b481f62",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 4",
    "content_id": "c_efdad9904ce9",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 5",
    "content_id": "c_c744659fc524",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  }
]
```

**Trial 2**

```json
[
  {
    "case": "run 1",
    "content_id": "c_00eb7bcab2f9",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 2",
    "content_id": "c_dc3e01efcc5a",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 3",
    "content_id": "c_16636d70213b",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 4",
    "content_id": "c_eefdfaba4671",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 5",
    "content_id": "c_773856aa51eb",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  }
]
```

**Trial 3**

```json
[
  {
    "case": "run 1",
    "content_id": "c_0e86cd65e959",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 2",
    "content_id": "c_b5aca8f195c0",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 3",
    "content_id": "c_19f36caaf0f1",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 4",
    "content_id": "c_e339124ced9e",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  },
  {
    "case": "run 5",
    "content_id": "c_d38191e08225",
    "expect": "one 200 + one 409, 1 review line",
    "http": {
      "overturned": 200,
      "upheld": 409
    },
    "review_lines": 1,
    "status_after": "overturned",
    "as_expected": true
  }
]
```

### 10. crashes are still traceable

**Trial 1**

```json
[
  {
    "case": "model signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_d5d549d12a9c",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_d5d549d12a9c",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "style signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_a0e1af484b4c",
    "logged_error_type": "ZeroDivisionError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_a0e1af484b4c",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "score combining crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_4f27f9771067",
    "logged_error_type": "KeyError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_4f27f9771067",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "appeal write crashes",
    "route": "/appeal",
    "content_id": "c_ef0f31a6c415",
    "expect": 500,
    "http": 500,
    "error_id": "e_3066b5e6c33e",
    "logged_error_type": "OSError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "decided",
    "status_after": "decided",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_3066b5e6c33e",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "review write crashes",
    "route": "/review",
    "content_id": "c_92acfce2f747",
    "expect": 500,
    "http": 500,
    "error_id": "e_244c237e9531",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "under_review",
    "status_after": "under_review",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_244c237e9531",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  }
]
```

**Trial 2**

```json
[
  {
    "case": "model signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_82882f61c039",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_82882f61c039",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "style signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_08a0c88ca17d",
    "logged_error_type": "ZeroDivisionError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_08a0c88ca17d",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "score combining crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_987143030dfb",
    "logged_error_type": "KeyError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_987143030dfb",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "appeal write crashes",
    "route": "/appeal",
    "content_id": "c_9f6da0cf4a2d",
    "expect": 500,
    "http": 500,
    "error_id": "e_f6ee49b1d548",
    "logged_error_type": "OSError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "decided",
    "status_after": "decided",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_f6ee49b1d548",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "review write crashes",
    "route": "/review",
    "content_id": "c_bba2bc262b45",
    "expect": 500,
    "http": 500,
    "error_id": "e_9038d23a76a1",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "under_review",
    "status_after": "under_review",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_9038d23a76a1",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  }
]
```

**Trial 3**

```json
[
  {
    "case": "model signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_20813e6aea5d",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_20813e6aea5d",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "style signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_0c0d832c06e2",
    "logged_error_type": "ZeroDivisionError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_0c0d832c06e2",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "score combining crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_e33ed85f15ec",
    "logged_error_type": "KeyError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_e33ed85f15ec",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "appeal write crashes",
    "route": "/appeal",
    "content_id": "c_83ddaa06ed8d",
    "expect": 500,
    "http": 500,
    "error_id": "e_dbe8ba402420",
    "logged_error_type": "OSError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "decided",
    "status_after": "decided",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_dbe8ba402420",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "review write crashes",
    "route": "/review",
    "content_id": "c_a14b75a39d1f",
    "expect": 500,
    "http": 500,
    "error_id": "e_ce0dc0c19abe",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "under_review",
    "status_after": "under_review",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_ce0dc0c19abe",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  }
]
```
