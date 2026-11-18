# Implementation Plan — HOLD-21 Overdue Hold Shelf

## Scope and approved decisions

This plan implements the approved `requirements.md`, `architecture.md`, and
`design-review.md` without changing the existing list or pickup contracts.
The overdue response is `{"holds":[...]}` with `id`, `title`, `patron`,
`readySince`, `status`, `phone`, and `waitingDays`; an empty result is
`{"holds":[]}`. Supplied `days` values must be positive integers, with
missing `days` defaulting to 7. The calculation accepts `YYYY-MM-DD`
server-local dates, includes only `waitingDays > days`, excludes malformed
dates without exposing sensitive data, and maps missing overdue-view phones to
`Not Found`. The page uses the agreed action, input, validation, failure
clearing, and retry behavior.

## Tasks

### T1 — Add the overdue validation and selection boundary

- **Outcome:** Introduce a focused overdue service/module under
  `src/holdshelf/` that validates an optional `days` query value, supplies
  the default of 7, calculates server-local calendar waiting days, filters
  only eligible ready holds, and maps the overdue response fields. Provide a
  clock/date seam so tests can anchor today without changing normal
  server-local behavior. Treat absent `readySince` and malformed dates as
  exclusions; log only a non-sensitive diagnostic for malformed dates.
- **Files to touch:** `src/holdshelf/overdue.py` (new); `src/holdshelf/catalog.py`
  only if the existing hold representation must safely preserve an absent
  `readySince`; `tests/test_holdshelf.py` for service-level coverage.
- **Depends on:** None.
- **Done when:** Unit coverage proves default and positive-integer windows,
  strict `waitingDays > days` behavior, the 18 November 2026 boundary
  examples, local-date calculation through the seam, ready/picked-up and
  absent/malformed `readySince` filtering, and `Not Found` phone mapping,
  without altering the existing catalog list representation.

### T2 — Expose the overdue service through the API

- **Outcome:** Add `GET /api/holds/overdue` to the existing handler, parse the
  query string without confusing an absent parameter with a supplied blank
  value, return the approved 400 error object for every invalid supplied
  value, and return the shared overdue result for valid requests. Preserve
  health, `GET /api/holds`, pickup status transitions, and their existing
  missing-phone behavior exactly.
- **Files to touch:** `src/holdshelf/server.py`; `tests/test_holdshelf.py`.
- **Depends on:** T1.
- **Done when:** Handler tests cover the default route, valid override,
  empty success, all invalid `days` categories (including valueless and
  repeated/malformed query input as appropriate to the chosen parser), the
  approved response envelope and fields, and regression coverage confirms
  `GET /api/holds` still returns a missing phone as JSON `null` and pickup
  behavior remains unchanged.

### T3 — Add the overdue controls and result view to the existing page

- **Outcome:** Extend the current page with an `Overdue Holds` action and a
  positive-integer `days` input defaulting to 7. Blank input uses 7; invalid
  input is reported before a request. Invoke the overdue endpoint on action,
  render waiting days and phone values, distinguish an empty successful result,
  and on failure clear overdue rows, show a distinct error, and provide Retry
  without disturbing the existing list and pickup controls.
- **Files to touch:** `src/holdshelf/static/index.html`; `tests/test_holdshelf.py`
  for page contract assertions.
- **Depends on:** T2.
- **Done when:** The page source contains the agreed control, endpoint
  request, pre-request validation, overdue fields including `Not Found`,
  no-results messaging, and retry/failure clearing logic; existing
  `/api/holds` loading and pickup flow remain present and separate.

### T4 — Complete end-to-end compatibility and acceptance coverage

- **Outcome:** Consolidate black-box `ShelfApp.handle` coverage for the
  approved acceptance criteria and edge cases, including state changes from
  pickup affecting subsequent overdue results and an empty catalog.
- **Files to touch:** `tests/test_holdshelf.py` (or a new
  `tests/test_overdue_holds.py` if separation is clearer).
- **Depends on:** T2 and T3; T1's clock seam and selection contract must be
  available.
- **Done when:** Tests demonstrate API/page parity for the same catalog,
  H-1042 inclusion and H-1048/H-0991 exclusion on the anchored date,
  missing-phone serialization, valid short-window behavior, invalid-window
  400 behavior, empty success, malformed/missing dates, and unchanged
  health/list/pickup routes.

## Blocked list

- **T2** is blocked until **T1** establishes the validator and overdue
  selection contract.
- **T3** is blocked until **T2** establishes the final endpoint contract.
- **T4** is blocked until **T2** and **T3** are complete so API, UI, and
  compatibility behavior can be exercised together.
- No task is blocked by a missing approved requirement or design decision.

## First task free to start

**T1 — Add the overdue validation and selection boundary.**
