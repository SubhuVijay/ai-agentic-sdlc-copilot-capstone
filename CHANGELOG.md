# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Overdue hold-shelf view and `GET /api/holds/overdue` endpoint for identifying ready holds beyond the pickup window, including waiting-day counts and `Not Found` phone values.
- Positive-integer pickup-window validation, empty-result handling, retry/error feedback, and acceptance coverage while preserving existing list and pickup behavior.

## [0.1.0] - 2026-11-17

### Added

- Agentic SDLC workspace for the Automated Documentation Sync capstone in GitHub Copilot: orchestrator and step custom agents, prompt files, custom instructions, the `agentic-sdlc` skill, and hooks.
- Hook tests for the SDLC status report, destructive-command guard, and secret-file guard.
