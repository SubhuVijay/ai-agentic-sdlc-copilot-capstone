---
name: Implementation
description: Implementation rules for the hold shelf under src/ and tests/.
applyTo: "src/**,tests/**"
---

# Implementation

- Implement only the task the user approved in `impl-plan.md`.
- Match behavior to `requirements.md` and the decisions in `design-review.md`.
- Name functions for the fact they collect or the failure they handle.
- Share duplicated logic. Do not copy the same check into a second function.
- Cover the happy path and the missing-field / `Not Found` case for the task you touch.
- Surface API failures, a missing hold, and an empty overdue list as a result the user can read.
- Extend `src/holdshelf`. Keep `GET /api/holds` and pickup working.

```text
# Bad
except Exception:
    pass

# Good
Return a result that names the failed call and still includes the holds that could be loaded.
```
