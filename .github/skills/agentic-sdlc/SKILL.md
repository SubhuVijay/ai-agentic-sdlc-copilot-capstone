---
name: agentic-sdlc
description: Runs the Agentic SDLC for the Lane Street Library hold shelf in GitHub Copilot. Use when the user mentions SDLC, the orchestrator, a custom agent, the user story, requirements.md, architecture.md, design-review.md, impl-plan.md, implementation, code review, verification, changelog, or a pull request for this hold shelf.
---

# Agentic SDLC

Custom agents perform the steps. The human approves each step. Commit only when the user asks.

## Active step

The active step is the first missing artifact, unless the user names a step.

| Step | Agent | Artifact | Guide |
| --- | --- | --- | --- |
| 1 Requirements | `requirements` | `requirements.md` | [requirements.md](requirements.md) |
| 2 Architecture | `architect` | `architecture.md` | [architecture.md](architecture.md) |
| 3 Design review | `design-reviewer` | `design-review.md` | [design-review.md](design-review.md) |
| 4 Implementation plan | `planner` | `impl-plan.md` | [impl-plan.md](impl-plan.md) |
| 5 Implementation | `implementer` | approved task in `src/` and `tests/` | [implementation.md](implementation.md) |
| 6 Code review | `code-reviewer` | `code-review.md` | [review.md](review.md) |
| 7 Verify | `verifier` | `verification-report.md` | [verify.md](verify.md) |
| 8 Pull request | `release` | PR description and `CHANGELOG.md` | [pull-request.md](pull-request.md) |

Story: `docs/user-story.md`. Agents: `.github/agents/`. Prompts: `.github/prompts/`.

## Orchestrator

`orchestrator` coordinates. It has no edit tool, so it cannot write the step files.

1. Read the repository root and name the active step.
2. Where the `agent` tool is available, call that one custom agent, then stop.
3. Where it is not available, including Visual Studio, point the user at that step's handoff or prompt file, then stop.
4. On `waiting`, show the questions. On `done`, show the summary and wait for approval. On `blocked`, report the blocker.
5. Start the next step only after the user approves.

## Step agents

A step agent follows its guide. It reads the files on disk, because a handoff starts a fresh request. It does not launch another custom agent. It ends with this status:

```text
step: <number>
agent: <agent name>
status: waiting | done | blocked
artifact: <path or none>
summary: <what was done or asked>
questions: <numbered questions, or none>
blockers: <what stopped the step, or none>
```

`waiting` means questions are open. `done` means the artifact is ready for approval. `blocked` means a prerequisite is missing.

## Hard stops

- Do not write `requirements.md` until the user has answered the clarifying questions.
- Do not write production code before `impl-plan.md` exists and the user has named the task.
- Do not invent missing documentation facts. Record `Not Found`.
- Do not print secrets, `.env` values, tokens, or credential file contents.
- Do not skip a gate because a later prompt was run.
- Do not perform a step inside `orchestrator`. Hand it to that step's custom agent.
- Do not start the next step before the user approves the current one.
