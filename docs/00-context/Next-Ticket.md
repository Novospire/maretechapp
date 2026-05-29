# Next Ticket — Maretech

## Title

Select next controlled Maretech implementation ticket

## Goal

Define the next small implementation ticket after BE-040 and after the agent operating layer has been merged.

## Allowed Files

* docs/00-context/Next-Ticket.md
* docs/00-context/Current-State.md
* docs/60-delivery/Done-Log.md if needed

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

## Acceptance Criteria

* Next implementation ticket is clearly selected.
* Scope is small.
* Allowed/forbidden files are clear.
* Verification commands are defined.
* Maretech non-negotiables remain visible.

## Verification Commands

```bash
git status --short
git diff --stat
git diff --name-only
```

## Known Non-Blockers

* Existing backend/API work is not part of this ticket.
* Existing technical debt is not part of this ticket.
* Local `__pycache__` files must be removed or ignored before commit.

## Stop Conditions

Stop if any non-docs file changes.

Stop if the task expands into implementation, backend, API, database, deployment, auth, pricing or UI work.
