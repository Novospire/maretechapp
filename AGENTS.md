# AGENTS.md

## Source of Truth

Use repository files as source of truth.

Chat history is guidance only.

Read first:

- README.md
- docs/00-context/Context-Pack.md
- docs/00-context/Operating-Protocol.md
- docs/30-architecture/Repo-Index.md
- docs/00-context/Current-State.md
- docs/00-context/Next-Ticket.md
- docs/00-context/Agent-Operating-Protocol.md

If a listed file does not exist yet, report it and continue only with existing source-of-truth files.

## Maretech Non-Negotiables

- Osmosis and Corrosion are two separate products under one app shell.
- Do not merge Osmosis and Corrosion flows, pricing, onboarding or analysis language.
- Maretech is not a survey tool.
- Maretech does not provide binding diagnoses.
- Output language must remain probabilistic: signal, risk, confidence, monitor, re-check, escalate.
- Do not use definitive diagnosis language such as “has osmosis”, “has corrosion”, “clear”, “certified”, or “survey result”.
- Async-only inference is required.
- App and marketing site workstreams must stay separate.

## Rules

- Never push directly to main.
- Use branch → PR → review → merge.
- One task = one small ticket.
- Do not expand scope without approval.
- Do not edit forbidden files.
- Show changed files and verification before done.
- Do not fix unrelated technical debt opportunistically.
- Do not mix docs, backend, API, mobile UI, marketing site and deployment in one ticket.

## Forbidden by Default

Unless explicitly approved, do not edit:

- secrets
- .env files
- local artifacts
- __pycache__
- node_modules
- build outputs
- package dependencies
- production config
- database migrations
- payment logic
- auth logic
- deployment config

## PR Requirements

Include:

- why
- scope
- non-scope
- changed files
- verification
- known warnings / non-blockers
- related ADRs or tickets when applicable

## Done Means

Done requires:

- changed files list
- diff summary
- verification output
- known warnings / non-blockers
- explicit statement that Maretech non-negotiables were not violated
