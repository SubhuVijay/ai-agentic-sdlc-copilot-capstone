# Code Review — HOLD-21

## Review scope and disposition

The implementation under `src/holdshelf/` and its relevant tests in
`tests/test_holdshelf.py` were reviewed against `requirements.md`,
`architecture.md`, `design-review.md`, and `impl-plan.md`. No production code
or tests were changed during this review. All review areas below are marked
with their disposition.

## Correctness — pass

`src/holdshelf/server.py` adds the overdue route without changing the existing
health, list, or pickup branches. `src/holdshelf/overdue.py` applies the
`ready` and `readySince` filters, excludes picked-up holds, uses the strict
`waitingDays > days` boundary, and maps a missing phone to `Not Found`.
`ShelfApp._today` provides the test seam while the service's default
`date.today()` uses the server's local date. The API envelope and empty result
match the approved architecture.

The acceptance tests in `tests/test_holdshelf.py` cover H-1042, H-1048,
H-0991, missing and malformed dates, the default and short windows, pickup
state changes, missing-phone serialization, and an empty catalog. The page in
`src/holdshelf/static/index.html` sends the same window to the API, renders
waiting days and phone values, and preserves the existing list and pickup
controls.

## Security — pass

`validate_days` in `src/holdshelf/overdue.py`, together with the duplicate
parameter check in `ShelfApp._overdue`, rejects non-positive, non-integer,
blank, malformed, and repeated `days` values before selection. The page uses
`textContent` for returned hold fields and error text rather than injecting
response data as HTML. `src/holdshelf/static/index.html` also uses
`encodeURIComponent` for the request value. No patron payload, phone number,
secret, or credential is written to the diagnostic log; malformed-date
logging in `overdue.py` is non-sensitive.

## Error Handling — pass

`ShelfApp._overdue` returns a deterministic 400 error for invalid windows and
a successful `{"holds": []}` for no matches. `select_overdue` excludes
missing and malformed `readySince` values rather than fabricating a duration.
The page clears overdue rows before loading and again on failure, distinguishes
failure from the no-results message, and provides a Retry action in
`loadOverdue` and `showOverdueError`. Empty catalogs are exercised by
`test_empty_success_and_empty_catalog` in `tests/test_holdshelf.py`.

The requirements explicitly leave missing-file fallback behavior unspecified;
the review therefore does not invent a fallback for the existing static-file
route.

## Test Coverage — pass

`tests/test_holdshelf.py` contains both focused service tests and black-box
`ShelfApp` acceptance tests. It verifies the approved date boundary and
strict comparison, default and override behavior, every listed invalid-window
category, duplicate query values, missing/malformed dates, missing phones,
empty results, pickup exclusion after a state transition, and compatibility
of `GET /api/holds` including its `null` phone representation. The page
contract test checks the action, input, endpoint, rendered fields,
no-results text, validation text, row clearing, and retry affordance.

The page assertions are source-contract tests rather than browser execution
tests, but the repository's existing standard-library test setup has no
browser harness; the API and service behavior are covered through the public
application interface.

## Code Clarity — pass

Responsibilities are separated into `validate_days` and `select_overdue` in
`src/holdshelf/overdue.py`, route handling in `src/holdshelf/server.py`, and
presentation behavior in `src/holdshelf/static/index.html`. Names such as
`select_overdue`, `clearOverdueRows`, `renderOverdue`, and
`showOverdueError` describe their behavior directly. The implementation is
small enough that the filtering, validation, and response mapping are
readable without relying on comments.

## DRY Principle — pass

The API and page share the API's single overdue-selection implementation:
`ShelfApp._overdue` calls `select_overdue`, while the page consumes that
response rather than reimplementing date filtering. Existing list and pickup
behavior remains in the catalog and is not duplicated by the overdue path.
The page's separate normal-list and overdue renderers have different
contracts and fields, so they are not misleading copies that require a
shared renderer.

## Dependency Safety — pass

`src/holdshelf/server.py` and `src/holdshelf/overdue.py` use only Python
standard-library modules. No new package, lockfile change, or third-party
dependency is introduced by the implementation, so there are no added
package versions requiring vulnerability review. This is consistent with the
standard-library technology choice in `architecture.md` and the repository
description in `README.md`.

## Overall disposition

No blocker or requirement gap was found. The implementation is suitable to
advance to Step 7 verification.
