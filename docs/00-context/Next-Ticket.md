# Next Ticket — Maretech

## Title

Add Maretech-specific agent operating layer

## Goal

Add short project-local files that help Claude Code, Codex and Antigravity work safely in the Maretech repo.

This is a docs-only setup ticket.

## Allowed Files

* AGENTS.md
* CLAUDE.md
* docs/00-context/Current-State.md
* docs/00-context/Next-Ticket.md
* docs/00-context/Agent-Operating-Protocol.md
* docs/00-context/Design-Reference.md
* .claude/commands/repo-safety.md
* .claude/commands/challenge.md
* .claude/commands/pr-review.md

## Forbidden Files

* app/
* tests/
* backend/API implementation files
* auth files
* database files
* migration files
* deployment files
* package files
* .env files
* README.md unless explicitly approved
* existing architecture/product docs unless explicitly approved

## Acceptance Criteria

* Agent operating layer files are added.
* PR remains docs-only.
* No application code changes.
* No generated/local files committed.
* Maretech non-negotiables are clearly visible to agents.
* App and marketing site workstreams remain separated.

## Verification Commands

```bash
git status --short
git diff --stat
git diff --name-only
```

## Known Non-Blockers

* Existing backend/API work is not part of this ticket.
* Existing technical debt is not part of this ticket.
* Local **pycache** files must be removed or ignored before commit.

## Stop Conditions

Stop if any non-docs file changes.

Stop if the task expands into implementation, backend, API, database, deployment, auth, pricing or UI work.
