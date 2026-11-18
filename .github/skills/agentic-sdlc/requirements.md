# Step 1 — Requirements

1. Load the story, then read it.
   - Run `python scripts/load_user_story.py`.
   - Do not open `config/jira.local.json` and do not print tokens. The script reads that file.
   - `source` may be `jira`, `confluence`, `word`, or `file`. A Word file can also be loaded with `python scripts/load_user_story.py --word <path-to.docx>`.
   - If there is no local config, keep the story already in `docs/user-story.md`.
2. Read `docs/user-story.md`. Ask the open questions in that story. Add any question that would change scope, data, or failure behavior. Number the questions. Stop and wait.
3. After the user answers, write `requirements.md` at the repository root with:
   - Context and goal
   - Functional requirements (`FR-1`, ...)
   - Non-functional requirements (`NFR-1`, ...)
   - Acceptance criteria
   - Error and edge cases: missing files, empty repos, API failures, and `Not Found`
   - Out of scope
   - Decisions taken from the user's answers
4. Show the draft in chat. Commit only after the user approves it and asks for the commit.
