# Current State — Maretech App

## Last Confirmed Baseline

Branch: main

Last confirmed commit:

d8cb11e docs: update done log for BE-040 (#29)

Current working branch:

docs/agent-operating-layer

## Current Status

Maretech already has an initial repo source-of-truth structure.

Existing source-of-truth files include:

* README.md
* docs/00-context/Context-Pack.md
* docs/00-context/Operating-Protocol.md
* docs/30-architecture/Repo-Index.md
* docs/60-delivery/Definition-of-Done.md
* docs/60-delivery/Done-Log.md

This PR adds the Maretech-specific agent operating layer.

## Completed

* Initial backend sprint documentation exists.
* Repo Index exists.
* Context Pack exists.
* Operating Protocol exists.
* Done Log has been updated through BE-040.
* Central AI Delivery Operating Protocol repo has been created separately.

## In Progress

* Add Maretech-specific agent operating files.
* Keep this PR docs-only.
* Prepare repo for safer Claude Code / Codex / Antigravity handoffs.

## Known Warnings / Non-Blockers

* Python `__pycache__` folders may appear locally.
* They must not be committed.
* Existing technical debt should not be fixed in this PR.

## Open Risks

* Mixing app and marketing site workstreams.
* Weakening Osmosis / Corrosion product separation.
* Accidentally introducing diagnosis or survey-replacement language.
* Letting AI agents touch backend/API/deployment files during docs setup.
* Expanding this docs PR into implementation work.

## Next Recommended Ticket

Add Maretech-specific agent operating layer files:

* AGENTS.md
* CLAUDE.md
* docs/00-context/Current-State.md
* docs/00-context/Next-Ticket.md
* docs/00-context/Agent-Operating-Protocol.md
* docs/00-context/Design-Reference.md
* .claude/commands/repo-safety.md
* .claude/commands/challenge.md
* .claude/commands/pr-review.md
