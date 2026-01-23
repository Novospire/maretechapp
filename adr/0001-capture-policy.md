# ADR 0001 — Capture Policy (photo slots) + Free Tier Limits

## Status
Accepted

## Context
Context-Pack v1.1 lists “Minimum photo set requirements per mode” as an open question.
We need a stable backend/mobile contract BEFORE implementation, without hardcoding product numbers in code.

## Decision
Introduce a “capture policy” configuration per mode:
- Defines required photo slots (point/angle) and maximum slots per tier.
- Mobile enforces the sequence based on the policy fetched from backend.
- Backend validates submissions against the same policy.

Initial MVP defaults (tunable via config):
- Corrosion:
  - Free tier: up to 5 points
  - Each point: 3 angles (slot types)
  - Paid tier: up to 10 points
- Osmosis:
  - Policy defined separately (paid-first), no free tier.

## Rationale
- Avoids refactors when business rules change.
- Keeps mode isolation while sharing a common mechanism.
- Enables consistent training/inference inputs.

## Consequences
Positive outcomes:
- Stable API + data model
- Product can tune without code changes

Negative outcomes / risks:
- Slight upfront complexity (policy endpoint + validation)

Mitigations:
- Keep policy schema minimal in MVP.

## Links
- Related docs: /docs/00-context/Context-Pack.md, /docs/20-ux/App-Map.md, /docs/20-ux/UI-Tickets.md
- Related ADRs: /adr/0000-template.md
