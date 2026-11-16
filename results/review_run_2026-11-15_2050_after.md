# Review run — after

- Produced by: `run_reviews.py` · scenarios: `scenarios.py::REVIEW_SCENARIOS`
- Service: `app.py::review`, `app.py::appeal` (in-process, Flask test client)
- Log for this run: `logs/review_eval_2026-11-15_2050.jsonl`
- 3 trials per criterion · 2026-11-15 20:52

Each cell is how many cases did what scenarios.py expected. Fill in
Target from `criteria.md` and the Verdict yourself.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 6. a review resolves an appeal |  | 5/5 | 5/5 | 5/5 |  |
| 7. only a reviewer can review |  | 5/5 | 5/5 | 5/5 |  |
| 8. a reviewed decision is final, and bad review requests change nothing |  | 10/10 | 10/10 | 10/10 |  |
| 9. two reviews at the same moment |  | 5/5 | 5/5 | 5/5 |  |
| 10. crashes are still traceable |  | 5/5 | 5/5 | 5/5 |  |

---

## Cases that didn't do what was expected

None.

---

## What actually came back

Real output, token redacted. The full log lines are in the log above.

### 6. a review resolves an appeal

**Trial 1**

```json
[
  {
    "case": "overturned (text 1)",
    "content_id": "c_b0e6535329e3",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_b0e6535329e3",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:50:49+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "upheld (text 1)",
    "content_id": "c_cf84d7e40331",
    "expect": "200, final_guess=ai",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "ai",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_cf84d7e40331",
      "final_guess": "ai",
      "final_label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:50:53+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "upheld (text 2)",
    "content_id": "c_9162be29c765",
    "expect": "200, final_guess=unsure",
    "http": 200,
    "original_guess": "unsure",
    "final_guess": "unsure",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_9162be29c765",
      "final_guess": "unsure",
      "final_label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "original_guess": "unsure",
      "reviewed_at": "2026-11-16T01:50:56+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "overturned (text 3)",
    "content_id": "c_e67c92b7975e",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "human",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_e67c92b7975e",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "human",
      "reviewed_at": "2026-11-16T01:51:01+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "overturned (text 1)",
    "content_id": "c_4bc329fc5ada",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_4bc329fc5ada",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:08+00:00",
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
    "content_id": "c_ebaa88b3938a",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_ebaa88b3938a",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:15+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "upheld (text 1)",
    "content_id": "c_51983b62245c",
    "expect": "200, final_guess=ai",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "ai",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_51983b62245c",
      "final_guess": "ai",
      "final_label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:21+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "upheld (text 2)",
    "content_id": "c_1a5ba77cc429",
    "expect": "200, final_guess=unsure",
    "http": 200,
    "original_guess": "unsure",
    "final_guess": "unsure",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_1a5ba77cc429",
      "final_guess": "unsure",
      "final_label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "original_guess": "unsure",
      "reviewed_at": "2026-11-16T01:51:24+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "overturned (text 3)",
    "content_id": "c_2910c8514a58",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "human",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_2910c8514a58",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "human",
      "reviewed_at": "2026-11-16T01:51:31+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "overturned (text 1)",
    "content_id": "c_d53315e347ab",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_d53315e347ab",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:35+00:00",
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
    "content_id": "c_b83fae49a4c6",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_b83fae49a4c6",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:36+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "upheld (text 1)",
    "content_id": "c_4743420b0849",
    "expect": "200, final_guess=ai",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "ai",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_4743420b0849",
      "final_guess": "ai",
      "final_label": "The text is likely AI as it shows patterns common in AI-generated text. We can't be certain and the check may be wrong especially about plain, simple writing. If you wrote this yourself and believe this is an error, you can submit an appeal for a member of our team to review.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:39+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "upheld (text 2)",
    "content_id": "c_356e2b30c2e0",
    "expect": "200, final_guess=unsure",
    "http": 200,
    "original_guess": "unsure",
    "final_guess": "unsure",
    "status_after": "upheld",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_356e2b30c2e0",
      "final_guess": "unsure",
      "final_label": "It is unclear whether this was written by a human or AI. Certain parts are consistent with human written text, and others are consistent with AI-generated text. If you wrote this yourself you don't need to do anything.",
      "original_guess": "unsure",
      "reviewed_at": "2026-11-16T01:51:45+00:00",
      "status": "upheld"
    }
  },
  {
    "case": "overturned (text 3)",
    "content_id": "c_f31e78791489",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "human",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_f31e78791489",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "human",
      "reviewed_at": "2026-11-16T01:51:51+00:00",
      "status": "overturned"
    }
  },
  {
    "case": "overturned (text 1)",
    "content_id": "c_9c1bf1bdfc08",
    "expect": "200, final_guess=human",
    "http": 200,
    "original_guess": "ai",
    "final_guess": "human",
    "status_after": "overturned",
    "review_lines": 1,
    "as_expected": true,
    "response": {
      "content_id": "c_9c1bf1bdfc08",
      "final_guess": "human",
      "final_label": "A member of our team reviwed your appeal and agreed with you that this writing was not AI generated.",
      "original_guess": "ai",
      "reviewed_at": "2026-11-16T01:51:54+00:00",
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
    "content_id": "c_6e03b035726f",
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
    "content_id": "c_5f888dd65e7a",
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
    "content_id": "c_0885af0310fe",
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
    "content_id": "c_6fc24974ee1f",
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
    "content_id": "c_97150013699e",
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
    "content_id": "c_de78329f4a41",
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
    "content_id": "c_d6c94d22af02",
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
    "content_id": "c_1380457089ae",
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
    "content_id": "c_86fc4453f598",
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
    "content_id": "c_0cbc2b518318",
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
    "content_id": "c_f9d90ec67646",
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
    "content_id": "c_fe052026e4a1",
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
    "content_id": "c_c8a0254e3516",
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
    "content_id": "c_56d566007a46",
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
    "content_id": "c_3c712eca00b3",
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
    "content_id": "c_e2c24e55f1f0",
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
    "content_id": "c_3642ffe8f448",
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
    "content_id": "c_6eace678ad49",
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
    "content_id": "c_9508c880d57f",
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
    "content_id": "c_603187113060",
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
    "content_id": "c_6c61d866cf38",
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
    "content_id": "c_4e01cfd8b736",
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
    "content_id": "c_dc5cba55b712",
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
    "content_id": "c_b341ad370850",
    "expect": 409,
    "http": 409,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "under_review",
      "error": "conflict",
      "message": "This decision has already been appealed and is waiting for review.",
      "reason": "conflict"
    }
  },
  {
    "case": "appeal an already reviewed item",
    "route": "/appeal",
    "content_id": "c_74a1f951d99a",
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
      "message": "This appeal has already been reviewed, and the decision was overturned.",
      "reason": "conflict"
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
    "content_id": "c_bb08fa6dc47e",
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
    "content_id": "c_b42b47e7d979",
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
    "content_id": "c_6e9458f4242a",
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
    "content_id": "c_24c5fc89c65b",
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
    "content_id": "c_0704e216cd4d",
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
    "content_id": "c_49b6a2c667a9",
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
    "content_id": "c_5c23b8978528",
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
    "content_id": "c_3ad78c4650df",
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
    "content_id": "c_c952cc93a530",
    "expect": 409,
    "http": 409,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "under_review",
      "error": "conflict",
      "message": "This decision has already been appealed and is waiting for review.",
      "reason": "conflict"
    }
  },
  {
    "case": "appeal an already reviewed item",
    "route": "/appeal",
    "content_id": "c_3e861b052c62",
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
      "message": "This appeal has already been reviewed, and the decision was overturned.",
      "reason": "conflict"
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
    "content_id": "c_077d0d44d20f",
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
    "content_id": "c_a15fdec1ed34",
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
    "content_id": "c_bb1a5a59e00a",
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
    "content_id": "c_c5224c9f5b35",
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
    "content_id": "c_ec30f4eafb16",
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
    "content_id": "c_474e4b5ee8ea",
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
    "content_id": "c_087643073590",
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
    "content_id": "c_de0820128713",
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
    "content_id": "c_2cbbdd84e6a7",
    "expect": 409,
    "http": 409,
    "status_before": "under_review",
    "status_after": "under_review",
    "item_lines_added": 0,
    "rejected_lines": 1,
    "as_expected": true,
    "response": {
      "current_status": "under_review",
      "error": "conflict",
      "message": "This decision has already been appealed and is waiting for review.",
      "reason": "conflict"
    }
  },
  {
    "case": "appeal an already reviewed item",
    "route": "/appeal",
    "content_id": "c_737573977ee7",
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
      "message": "This appeal has already been reviewed, and the decision was overturned.",
      "reason": "conflict"
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
    "content_id": "c_40613b6ed6b2",
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
    "content_id": "c_10a0ab0973ba",
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
    "content_id": "c_9204c04bb818",
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
    "content_id": "c_20d4fbe1a5ee",
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
    "content_id": "c_4358538bb5e0",
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
    "content_id": "c_c1e65fea197a",
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
    "content_id": "c_c6f9f85f3e27",
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
    "content_id": "c_afb9617502cf",
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
    "content_id": "c_cda784736c31",
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
    "content_id": "c_652ceff24119",
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
    "content_id": "c_bc3baf7693ce",
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
    "content_id": "c_fd4becb8d689",
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
    "content_id": "c_61e8672f6d7a",
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
    "content_id": "c_4f931a5e611b",
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
    "content_id": "c_d796469c0769",
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
    "error_id": "e_b36098106b79",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_b36098106b79",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "style signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_4ce7934f89fb",
    "logged_error_type": "ZeroDivisionError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_4ce7934f89fb",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "score combining crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_bfb2052d7d1a",
    "logged_error_type": "KeyError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_bfb2052d7d1a",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "appeal write crashes",
    "route": "/appeal",
    "content_id": "c_04ebcc9c0cf4",
    "expect": 500,
    "http": 500,
    "error_id": "e_8b34e0d6ba5c",
    "logged_error_type": "OSError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "decided",
    "status_after": "decided",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_8b34e0d6ba5c",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "review write crashes",
    "route": "/review",
    "content_id": "c_180854af9e18",
    "expect": 500,
    "http": 500,
    "error_id": "e_50d28c53b70c",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "under_review",
    "status_after": "under_review",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_50d28c53b70c",
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
    "error_id": "e_dd03ff5c1f8c",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_dd03ff5c1f8c",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "style signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_a48e2303ac07",
    "logged_error_type": "ZeroDivisionError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_a48e2303ac07",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "score combining crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_1b4dfe811243",
    "logged_error_type": "KeyError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_1b4dfe811243",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "appeal write crashes",
    "route": "/appeal",
    "content_id": "c_82bc6a5d89bf",
    "expect": 500,
    "http": 500,
    "error_id": "e_24337fde00d5",
    "logged_error_type": "OSError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "decided",
    "status_after": "decided",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_24337fde00d5",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "review write crashes",
    "route": "/review",
    "content_id": "c_dcf19cad69e9",
    "expect": 500,
    "http": 500,
    "error_id": "e_e743b3731e02",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "under_review",
    "status_after": "under_review",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_e743b3731e02",
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
    "error_id": "e_fc8e1c50aa47",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_fc8e1c50aa47",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "style signal crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_5785c7becc43",
    "logged_error_type": "ZeroDivisionError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_5785c7becc43",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "score combining crashes",
    "route": "/submit",
    "content_id": null,
    "expect": 500,
    "http": 500,
    "error_id": "e_ef9f3409baf5",
    "logged_error_type": "KeyError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": null,
    "status_after": null,
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_ef9f3409baf5",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "appeal write crashes",
    "route": "/appeal",
    "content_id": "c_6872576f0f25",
    "expect": 500,
    "http": 500,
    "error_id": "e_0aa70e1c787d",
    "logged_error_type": "OSError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "decided",
    "status_after": "decided",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_0aa70e1c787d",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  },
  {
    "case": "review write crashes",
    "route": "/review",
    "content_id": "c_d9c621160a8f",
    "expect": 500,
    "http": 500,
    "error_id": "e_6839b48b5169",
    "logged_error_type": "RuntimeError",
    "logged_where": "run_reviews.py:280",
    "error_lines": 1,
    "status_before": "under_review",
    "status_after": "under_review",
    "as_expected": true,
    "response": {
      "error": "internal_error",
      "error_id": "e_6839b48b5169",
      "message": "Something went wrong on our side. Nothing was decided. Quote this error_id if you report it."
    }
  }
]
```
