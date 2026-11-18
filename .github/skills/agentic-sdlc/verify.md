# Step 7 — Verify

Prerequisite: `code-review.md` has no open blocker the user still wants fixed.

1. Run the full test suite, unit and integration, with `python -m unittest discover -s tests -v`. Record the command and the full output. Hook tests are already in `tests/`. Product tests added in Step 5 are part of the same run.
2. Check the hold shelf against `requirements.md`:
   - The existing list and pickup action still behave as they do now.
   - The long-waiting view and `GET /api/holds/overdue` match the approved rules.
   - A missing phone is the text `Not Found` where the requirements require it.
   - Secrets, tokens, and `.env` values are absent.
3. Write `verification-report.md` with the command, the pass or fail result, and any content-quality failures.
4. Fix in-scope failures, re-run, and replace the recorded output. Ask the user before widening the fix past the approved tasks.
