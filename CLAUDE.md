# CLAUDE.md

## Project Memory

This file gives Claude Code short Maretech-specific operating rules.

Do not treat chat history as source of truth.

Read first:

- AGENTS.md
- README.md
- docs/00-context/Context-Pack.md
- docs/00-context/Operating-Protocol.md
- docs/30-architecture/Repo-Index.md
- docs/00-context/Current-State.md
- docs/00-context/Next-Ticket.md

If a file does not exist yet, report it.

## Claude Code Rules

- Start with repo safety checks.
- Read only relevant files.
- Plan before non-trivial edits.
- State intended files before editing.
- Show diff and verification before done.
- Do not perform opportunistic refactors.
- Do not silently fix unrelated technical debt.
- Do not touch backend, auth, payments, database, deployment or package files unless explicitly in scope.

## Maretech Boundaries

- Osmosis and Corrosion are separate products under one app shell.
- No diagnosis language.
- Not a survey replacement.
- Use probabilistic visual-signal language only.
- Async-only inference.
- App and marketing site workstreams stay separate.
