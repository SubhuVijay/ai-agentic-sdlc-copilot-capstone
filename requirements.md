# Requirements — Overdue Hold Shelf

## Context and goal

Lane Street Library's existing hold shelf application needs to help librarians
identify ready holds that have remained on the shelf beyond the pickup window.
The feature must support contacting those patrons and freeing shelf space
without replacing the existing hold list or pickup action.

Story: HOLD-21 — Show holds that have waited too long.

## Assumptions

- The existing application, data model, routes, and page remain the source of
  existing behavior unless explicitly changed below.
- The server's local timezone is used to determine today and to calculate
  waiting days.
- The exact response envelope/property names for the new API are **Not Found**
  in the story and are therefore not specified by these requirements.
- The exact UI control, visual design, and client-side loading mechanism are
  **Not Found** beyond the behavior described below.
- The behavior for malformed or unparseable `readySince` values is **Not
  Found**; this requirement does not invent a fallback.
- The repository's deployment, persistence, authentication, and observability
  requirements are **Not Found**.

## Functional requirements

### FR-1 — Overdue hold selection

The application shall provide a view on the existing page that shows only
holds satisfying all of the following:

- `status` is `ready`;
- `readySince` is present; and
- the hold has waited longer than the configured pickup window.

Picked-up holds shall not appear in the overdue result.

### FR-2 — Pickup window

The default pickup window shall be 7 days.

The overdue API shall accept an optional query parameter named `days`, such as
`days=7`, to override the default. The page's overdue view shall use the same
window behavior.

Only positive integer values are valid. Missing `days` uses the default of 7;
the following values shall be rejected with HTTP 400 rather than guessed:

- zero;
- negative integers;
- decimal values;
- non-numeric values;
- malformed values; and
- a missing value when the parameter is supplied without an integer.

The exact clear-error response schema and wording are **Not Found**, but the
400 response shall clearly identify that the window value is invalid.

### FR-3 — Waiting-day calculation

For each included hold, the application shall show the number of days the
hold has been waiting, counted from `readySince` to today.

Today and the calculation shall use the server's local timezone. The exact
rounding and date parsing rules beyond this calendar-day requirement are **Not
Found**.

### FR-4 — Patron phone

The overdue view shall show the patron phone for each included hold.

When a patron has no phone, the value shown shall be the literal string
`Not Found`. The new API shall also return the literal JSON string `"Not
Found"` for a missing phone, rather than JSON `null`.

### FR-5 — Overdue API

The application shall add:

`GET /api/holds/overdue`

The endpoint shall return the same set of overdue holds represented by the
page's overdue view, including the waiting-days value and phone value.

An empty result shall be a successful response representing that no ready hold
is past the configured window. The exact empty-response shape is **Not Found**.

### FR-6 — Existing holds API compatibility

`GET /api/holds` shall remain exactly unchanged, including its existing
behavior and representation of missing phone values.

### FR-7 — Existing functionality

The existing hold list and pickup action shall continue to work. This feature
shall not change how a hold is marked picked up.

## Non-functional requirements

### NFR-1 — Compatibility

The change shall be additive to the existing hold shelf application. Existing
routes and existing consumers of `GET /api/holds` shall not require changes.

### NFR-2 — Deterministic validation

Invalid `days` values shall consistently produce HTTP 400 and shall never
silently fall back to a different window or return a guessed hold list.

### NFR-3 — Clear user feedback

The page shall make the overdue-holds action and its result understandable to
the librarian, including the no-results case and invalid-window error.

### NFR-4 — Timezone consistency

The API and page shall use the server's local timezone consistently when
determining today and calculating waiting days.

### NFR-5 — Error handling

The new endpoint and page shall preserve clear failure behavior. Exact
logging, retry, timeout, and API error-handling requirements are **Not Found**.

## Acceptance criteria

1. With no `days` query parameter, the overdue behavior uses a 7-day window.
2. With a positive integer such as `days=7`, the endpoint and page use that
   configured window.
3. On 18 November 2026 with a 7-day window, a ready hold from 2 November
   (H-1042) is included.
4. On 18 November 2026 with a 7-day window, a ready hold from 16 November
   (H-1048) is excluded.
5. A picked-up hold such as H-0991 is excluded.
6. A ready hold with no `readySince` is excluded.
7. Each included hold displays its waiting-day count from `readySince` to
   today, using the server local timezone.
8. A missing phone is represented by the literal string `Not Found` both in
   the overdue API response and on the overdue page.
9. A valid request with no overdue holds returns an empty successful result,
   rather than an error or guessed list.
10. Missing `days` defaults to 7, while `days=0`, negative, decimal,
    non-numeric, malformed, or otherwise non-positive/non-integer values return
    HTTP 400 with a clear error.
11. `GET /api/holds` remains exactly unchanged.
12. The existing list and pickup behavior continue to work.

## Error and edge cases

- **Invalid window:** Return HTTP 400 for every supplied `days` value that is
  not a positive integer. Do not guess a list. The precise error payload is
  **Not Found**.
- **No `days` parameter:** Use the default 7-day window.
- **Ready hold without `readySince`:** Exclude it from the overdue result.
  The waiting-days value for such a hold is not applicable because the hold is
  excluded.
- **Missing phone:** Return and display `Not Found`.
- **Picked-up hold:** Exclude it even if its `readySince` date is old.
- **No overdue holds:** Return a successful empty result and communicate that
  no ready hold is past the window.
- **Missing files or required application data:** Required behavior and
  fallback handling are **Not Found**. Do not invent substitute data.
- **Empty repository or empty hold collection:** An empty hold collection
  produces an empty successful overdue result; repository/bootstrap behavior is
  **Not Found**.
- **API failure while loading the page:** The exact retry, fallback, and user
  messaging behavior is **Not Found**. The page must not present a guessed
  overdue list.
- **Malformed `readySince`:** Handling is **Not Found**. No fallback waiting
  duration is specified.

## Out of scope

- Sending email or SMS.
- Connecting to the city library circulation system.
- Changing how a hold is marked picked up.
- Fines, renewals, or checkout.
- Replacing the existing hold list.
- Changing `GET /api/holds`.

## Decisions taken from the user's answers

1. The default pickup window is 7 days; it is editable with a positive-integer
   query parameter such as `days=7`.
2. The server local timezone decides today and waiting-day calculations.
3. Ready holds without `readySince` are excluded.
4. Missing phone values are the literal string `Not Found` in the API and on
   the page.
5. `GET /api/holds` remains exactly unchanged.
6. Only positive integers are accepted for the window. Missing, zero,
   negative, decimal, non-numeric, and malformed values are rejected with
   HTTP 400; a missing parameter means the default 7-day window.
