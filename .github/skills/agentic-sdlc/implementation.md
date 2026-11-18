# Step 5 — Implementation

Prerequisite: the user approved `impl-plan.md` and named the task to build.

1. Implement that task only.
2. Follow `requirements.md`, `architecture.md`, and the decisions in `design-review.md`.
3. Put application code in `src/` and tests in `tests/`.
4. Validate user input. Keep secrets out of output and logs. Write `Not Found` when the story says a missing phone or date cannot be determined.
5. Handle API failures, a missing hold, and an empty overdue list with a readable result, not an uncaught stack trace. Extend `src/holdshelf`. Do not replace the existing list or pickup action.
6. Add tests for the happy path and for the missing-field / `Not Found` cases this task introduces.
7. When the task's definition of done is met, summarize the files changed and wait before the next task.
