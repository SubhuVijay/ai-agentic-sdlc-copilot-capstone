# Design Review — HOLD-21

## Review scope

This review covers the approved `requirements.md` and `architecture.md` for
the additive overdue-holds capability. The existing implementation was
inspected to identify compatibility, failure-path, and testability risks. No
production code or implementation plan is included.

## Approved baseline

The following decisions are already approved in the requirements and
architecture and are not reopened by this review:

- The default pickup window is 7 days.
- A supplied `days` value must be a positive integer; invalid values return
  HTTP 400, while an absent value uses the default.
- The server local timezone determines today and waiting-day calculations.
- Ready holds without `readySince` are excluded.
- Missing overdue-view phone values are the literal `Not Found`.
- `GET /api/holds` remains unchanged, including its `null` phone values.
- Existing list and pickup behavior remains intact.

The human resolved all findings in this review. The decisions are recorded
below and the corresponding agreed changes are reflected in
`architecture.md`.

## Findings requiring decisions

### DR-1 — Resolved decision: new API response contract

The requirements and architecture leave the successful response envelope,
property names, and empty-result shape as `Not Found`. The existing
application uses a `{"holds": [...]}` envelope, but the new endpoint is a
new consumer contract and the page cannot be reviewed for compatibility
without knowing whether it will consume that shape. This also leaves the
waiting-days property name and the representation of each overdue hold
undecided.

**Decision:** `GET /api/holds/overdue` returns
`{"holds":[{id,title,patron,readySince,status,phone,waitingDays}]}`.
An empty successful response is `{"holds":[]}`. Invalid windows return HTTP
400 with `{"error":"days must be a positive integer"}`.

### DR-2 — Resolved decision: malformed `readySince`

The catalog currently stores `readySince` as a string, and the new selection
service must parse it to calculate calendar days. The requirements explicitly
leave malformed or unparseable values as `Not Found`, so an implementation
could accidentally crash the endpoint, omit the record, or return a guessed
duration. The architecture repeats the gap but does not choose a safe
failure behavior.

**Decision:** Exclude holds with malformed `readySince` values and log a
non-sensitive diagnostic. No fabricated waiting-days value is returned.

### DR-3 — Resolved decision: calendar-day parsing and boundary behavior

The current seed data uses date-only ISO strings, while the requirements
mention date parsing and rounding rules beyond the calendar-day requirement
as `Not Found`. It is therefore unclear how date-times, offsets, or a
ready-since value at the local-day boundary are converted before comparing
the wait with the configured window. This affects both inclusion and the
reported waiting-days value.

**Decision:** Accept `readySince` in `YYYY-MM-DD` server-local calendar-date
format and calculate the calendar-day difference. Include a hold only when
`waitingDays > days`.

### DR-4 — Resolved decision: page control and request behavior

The page must use the same window behavior as the API, but the control,
whether the window is editable on the page, and the client loading sequence
are all `Not Found`. The existing page only renders the existing list and
does not have an overdue action. Without a decision, the page could omit the
override, send an invalid or stale value, or fail to make the overdue action
understandable.

**Decision:** Add an `Overdue Holds` action and a positive-integer `days`
input defaulting to 7. Invoke the request on the action; blank input uses 7.
Invalid input is shown before a request is made. Existing list and pickup
controls are preserved.

### DR-5 — Resolved decision: API failure handling

The architecture correctly says the page must not show a guessed list when
the API fails, but the requirements leave retry, fallback, and exact user
messaging as `Not Found`. The current page catches a failed initial request
with a generic message, so the overdue action needs an explicit failure
state that cannot be confused with a successful empty result.

**Decision:** On failure, clear overdue rows, show a distinct error, and
provide Retry. Never show stale overdue rows.

## Notes

### DR-6 — Note: deterministic time needs a test seam

The API must use the server's local timezone, and the acceptance examples
are anchored to 18 November 2026. The current code has no clock abstraction.
The design review recommends a testable way to provide the current local date
to the overdue calculation, while retaining the server local timezone in
normal operation. This is a testability recommendation, not a new product
requirement.

### DR-7 — Note: compatibility coverage should protect the existing API

The existing tests verify that `GET /api/holds` returns a missing phone as
JSON `null` and that pickup behavior works. The implementation should retain
those regression checks while adding overdue tests for ready/picked-up
filtering, missing `readySince`, missing phone mapping, default and valid
windows, invalid values, empty results, and date boundaries.

## Review outcome

All findings are resolved. The approved decisions are reflected in
`architecture.md`; no implementation plan is requested or provided in this
step.
