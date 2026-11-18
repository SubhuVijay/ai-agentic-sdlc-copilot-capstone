# Agentic SDLC — Lane Street Library hold shelf

This repository is the GitHub Copilot workspace for the Lane Street Library hold shelf. Copilot custom agents run the delivery lifecycle. The human approves every step. The sample app in `src/holdshelf` already lists holds and marks them picked up. The story adds the long-waiting view on top of it.

Story: `docs/user-story.md`. Procedure: `.github/skills/agentic-sdlc/SKILL.md`.

## Order

Write these files at the repository root, in order, and only after the previous one is approved:

1. `requirements.md` — after the user answers the clarifying questions
2. `architecture.md`
3. `design-review.md`, then update `architecture.md` for agreed changes
4. `impl-plan.md` — dependency order, with blocked tasks named
5. One approved task at a time under `src/` and `tests/`
6. `code-review.md`
7. `verification-report.md`
8. `CHANGELOG.md` entry and a pull request — only when the user asks

## Gates

- Ask the clarifying questions and wait for answers before writing `requirements.md`.
- Do not start a later step while an earlier artifact is missing.
- Do not write production code before `impl-plan.md` exists and the user names the task. Extend `src/holdshelf`. Do not replace the existing list or pickup action.
- Do not skip a gate because a later prompt was run.
- Record unknown facts as `Not Found`.
- Commit, push, and open a pull request only when the user asks.
- Do not print secrets, tokens, `.env` values, or credential-file contents.

## Who does the work

| Step | Custom agent | Prompt | Artifact |
| --- | --- | --- | --- |
| Coordinate | `orchestrator` | `/sdlc-status` | none — it does not write step files |
| 1 Requirements | `requirements` | `/requirements` | `requirements.md` |
| 2 Architecture | `architect` | `/architecture` | `architecture.md` |
| 3 Design review | `design-reviewer` | `/design-review` | `design-review.md` |
| 4 Implementation plan | `planner` | `/implementation-plan` | `impl-plan.md` |
| 5 Implementation | `implementer` | `/implementation` | the named task in `src/` and `tests/` |
| 6 Code review | `code-reviewer` | `/code-review` | `code-review.md` |
| 7 Verify | `verifier` | `/verify` | `verification-report.md` |
| 8 Pull request | `release` | `/pull-request` | PR description and `CHANGELOG.md` |

In Visual Studio, select `orchestrator` in Copilot Chat, or run a prompt file with `/`. The orchestrator names the active step. Continue that step with its handoff button or its prompt. Visual Studio does not spawn subagents, so the step agent runs in the chat when you select it.

Where the `agent` tool exists, `orchestrator` may call the active step's custom agent once, then stop and wait.

```markdown
# Bad
Implemented the CLI because the story mentioned a local tool.

# Good
Asked the six open questions in docs/user-story.md and waited for answers
before drafting requirements.md.
```
