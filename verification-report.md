# Verification Report — HOLD-21

## Scope and prerequisites

- Approved artifacts read: `requirements.md`, `architecture.md`,
  `design-review.md`, `impl-plan.md`, and `code-review.md`.
- Story and guidance read: `docs/user-story.md`,
  `.github/skills/agentic-sdlc/SKILL.md`,
  `.github/skills/agentic-sdlc/verify.md`, and
  `.github/instructions/sdlc-artifacts.instructions.md`.
- `code-review.md` is present and reports no open blocker.
- Implementation inspected: `src/holdshelf/catalog.py`,
  `src/holdshelf/overdue.py`, `src/holdshelf/server.py`, and
  `src/holdshelf/static/index.html`.
- Tests inspected: `tests/test_holdshelf.py` and the repository hook/config
  tests.

## Test execution

Command:

```text
python -m unittest discover -s tests -v
```

Result: **PASS** — exit code `0`; 40 tests ran and all passed.

Full output:

```text
test_cli_and_vs_code_payloads (test_guard_secrets.GuardSecretsTests.test_cli_and_vs_code_payloads) ... ok
test_ordinary_and_example_files_are_allowed (test_guard_secrets.GuardSecretsTests.test_ordinary_and_example_files_are_allowed) ... ok
test_secret_files_are_denied (test_guard_secrets.GuardSecretsTests.test_secret_files_are_denied) ... ok
test_cli_payload_with_tool_args_string (test_guard_shell.GuardShellTests.test_cli_payload_with_tool_args_string) ... ok
test_decision_is_mirrored_for_vs_code (test_guard_shell.GuardShellTests.test_decision_is_mirrored_for_vs_code) ... ok
test_destructive_git_asks_for_confirmation (test_guard_shell.GuardShellTests.test_destructive_git_asks_for_confirmation) ... ok
test_env_example_files_are_allowed (test_guard_shell.GuardShellTests.test_env_example_files_are_allowed) ... ok
test_malformed_input_fails_open (test_guard_shell.GuardShellTests.test_malformed_input_fails_open) ... ok
test_ordinary_git_commands_are_allowed (test_guard_shell.GuardShellTests.test_ordinary_git_commands_are_allowed) ... ok
test_secret_reads_are_denied (test_guard_shell.GuardShellTests.test_secret_reads_are_denied) ... ok
test_vs_code_payload_with_tool_input_object (test_guard_shell.GuardShellTests.test_vs_code_payload_with_tool_input_object) ... ok
test_health (test_holdshelf.HoldShelfTests.test_health) ... ok
test_lists_holds_and_keeps_a_missing_phone_as_null (test_holdshelf.HoldShelfTests.test_lists_holds_and_keeps_a_missing_phone_as_null) ... ok
test_overdue_api_contract_and_validation (test_holdshelf.HoldShelfTests.test_overdue_api_contract_and_validation) ... ok
test_overdue_service_uses_strict_window_and_maps_missing_phone (test_holdshelf.HoldShelfTests.test_overdue_service_uses_strict_window_and_maps_missing_phone) ... Excluding a hold with malformed readySince
Excluding a hold with malformed readySince
ok
test_page_contract_includes_overdue_controls_and_failure_states (test_holdshelf.HoldShelfTests.test_page_contract_includes_overdue_controls_and_failure_states) ... ok
test_page_loads_the_hold_api (test_holdshelf.HoldShelfTests.test_page_loads_the_hold_api) ... ok
test_pickup_marks_the_hold_and_rejects_a_second_pickup (test_holdshelf.HoldShelfTests.test_pickup_marks_the_hold_and_rejects_a_second_pickup) ... ok
test_unknown_hold_returns_404 (test_holdshelf.HoldShelfTests.test_unknown_hold_returns_404) ... ok
test_unknown_path_returns_404 (test_holdshelf.HoldShelfTests.test_unknown_path_returns_404) ... ok
test_anchored_default_window_includes_only_the_approved_hold (test_holdshelf.OverdueAcceptanceTests.test_anchored_default_window_includes_only_the_approved_hold) ... Excluding a hold with malformed readySince
ok
test_api_and_page_expose_the_same_overdue_contract (test_holdshelf.OverdueAcceptanceTests.test_api_and_page_expose_the_same_overdue_contract) ... Excluding a hold with malformed readySince
ok
test_empty_success_and_empty_catalog (test_holdshelf.OverdueAcceptanceTests.test_empty_success_and_empty_catalog) ... Excluding a hold with malformed readySince
ok
test_existing_health_list_and_pickup_routes_remain_compatible (test_holdshelf.OverdueAcceptanceTests.test_existing_health_list_and_pickup_routes_remain_compatible) ... ok
test_invalid_windows_return_a_clear_bad_request (test_holdshelf.OverdueAcceptanceTests.test_invalid_windows_return_a_clear_bad_request) ... ok
test_missing_and_malformed_dates_are_excluded (test_holdshelf.OverdueAcceptanceTests.test_missing_and_malformed_dates_are_excluded) ... Excluding a hold with malformed readySince
ok
test_pickup_changes_subsequent_overdue_results (test_holdshelf.OverdueAcceptanceTests.test_pickup_changes_subsequent_overdue_results) ... Excluding a hold with malformed readySince
Excluding a hold with malformed readySince
ok
test_short_window_includes_recent_ready_hold_and_serializes_missing_phone (test_holdshelf.OverdueAcceptanceTests.test_short_window_includes_recent_ready_hold_and_serializes_missing_phone) ... Excluding a hold with malformed readySince
ok
test_blank_jira_token_is_rejected (test_jira_config.StorySourceTests.test_blank_jira_token_is_rejected) ... ok
test_confluence_storage_becomes_text (test_jira_config.StorySourceTests.test_confluence_storage_becomes_text) ... ok
test_example_config_has_no_token (test_jira_config.StorySourceTests.test_example_config_has_no_token) ... ok
test_file_source_does_not_need_a_token (test_jira_config.StorySourceTests.test_file_source_does_not_need_a_token) ... ok
test_flat_jira_config_strips_the_base_url (test_jira_config.StorySourceTests.test_flat_jira_config_strips_the_base_url) ... ok
test_missing_config_leaves_the_story_in_place (test_jira_config.StorySourceTests.test_missing_config_leaves_the_story_in_place) ... ok
test_missing_file_names_the_example (test_jira_config.StorySourceTests.test_missing_file_names_the_example) ... ok
test_word_document_becomes_markdown (test_jira_config.StorySourceTests.test_word_document_becomes_markdown) ... ok
test_cli_emits_additional_context_in_both_shapes (test_sdlc_context.GateReportTests.test_cli_emits_additional_context_in_both_shapes) ... ok
test_completed_planning_gates (test_sdlc_context.GateReportTests.test_completed_planning_gates) ... ok
test_missing_gates_point_at_requirements (test_sdlc_context.GateReportTests.test_missing_gates_point_at_requirements) ... ok
test_next_gate_is_the_first_missing_artifact (test_sdlc_context.GateReportTests.test_next_gate_is_the_first_missing_artifact) ... ok

----------------------------------------------------------------------
Ran 40 tests in 0.461s

OK
No config/jira.local.json. Using docs/user-story.md
Wrote C:\Users\SUBRAM~1\AppData\Local\Temp\tmp4dxni5p9\user-story.md from C:\Users\SUBRAM~1\AppData\Local\Temp\tmp4dxni5p9\story.docx
```

## Acceptance and compatibility checks

**PASS.** The implementation and acceptance tests cover:

- default 7-day and positive-integer window overrides;
- the 18 November 2026 boundary (`H-1042` included and `H-1048` excluded);
- picked-up and missing or malformed `readySince` exclusions;
- strict `waitingDays > days` selection and server-local date seam;
- `Not Found` phone mapping for the overdue API/page;
- successful empty results;
- deterministic HTTP 400 handling for invalid and repeated `days` values;
- unchanged `GET /api/holds` null-phone behavior and pickup transitions;
- page controls, validation, no-results messaging, failure clearing, and
  retry behavior; and
- secret-file and shell-guard coverage. No secrets, tokens, or `.env` values
  were exposed by the verification.

## Documentation snapshot

Snapshot directory check command:

```text
Test-Path docs/output
```

Result: **Not Found** — `docs/output/` is absent.

Snapshot generator/check command: **Not Found**. No snapshot generator or
snapshot-check command is present in the repository's documented checks or
available scripts. The snapshot therefore could not be generated or compared.
This is a documentation-verification limitation; no production code, tests, or
other SDLC artifact was changed to compensate.

## Content-quality findings

- Automated tests: **PASS**.
- Acceptance and compatibility checks: **PASS**.
- Documentation snapshot generation/check: **Not Found** because the snapshot
  and its generator/check command are unavailable.
- No in-scope implementation failure was found to fix.
