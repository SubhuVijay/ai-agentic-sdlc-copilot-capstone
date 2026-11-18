---
name: Secrets and input
description: Keep secrets out of chat, logs, commits, and the documentation snapshot. Validate user-supplied paths and URLs.
applyTo: "**"
---

# Secrets and input

- Do not read, print, or commit `.env`, `config/jira.local.json`, key files, or credential files. `.env.example` and `config/jira.example.json` may be read.
- Do not echo environment variables or tokens into chat, logs, or the documentation snapshot.
- Validate user-supplied paths and URLs. Reject a path that escapes the directory the user named.
- When a required fact is missing, write `Not Found` instead of a placeholder secret or a guess.

```text
# Bad
metadata_url = "https://example.test/api?token=abc123"

# Good
Read the metadata URL from configuration. If it is unset, record Not Found.
```
