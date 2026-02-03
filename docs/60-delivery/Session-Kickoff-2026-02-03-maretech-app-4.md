# MARETECHAPP — Session Kickoff (Maretech App - 4)

**Date (Europe/Istanbul):** 2026-02-03  
**Repo:** Novospire/maretechapp  
**Baseline (main@HEAD):** 398b3f4 — Merge PR #8 (BE-020 Capture Policy endpoint)

## Working Rule (Source of Truth)
Repo documents are the only source of truth. Chat content is valid only if reflected in the repo.

## Non-negotiables (Locked)
- Osmosis and Corrosion are isolated products (no flow/schema mixing).
- No diagnosis language; outputs are non-binding.
- Async-only inference (no blocking calls).
- No scope expansion; ticket-only work.
- Never push directly to main — every change via PR.
- PR description must include: Repo Read Log + Scope (done/not) + Files changed.

## Completed as of baseline
### BE-010 Auth + API skeleton (merged PR #1)
- /auth/register, /auth/login, /auth/logout, /auth/me
- In-memory user store + token revocation list
- JWT secret required env: MARETECH_JWT_SECRET

### BE-012 CI smoke (pytest) (merged PR #5)
- GitHub Actions ci.yml → pip install -r requirements.txt + pytest -q
- CI env: PYTHONPATH=. and MARETECH_JWT_SECRET=test-secret

### BE-013 Auth token uniqueness (jti) (merged PR #6)
- Token uniqueness fixed; tests pass

### BE-014 README quickstart verify (README-only) (merged PR #7)
- Quickstart commands verified and added to README

### Delivery docs added (main)
- docs/60-delivery/Done-Log.md
- docs/60-delivery/Definition-of-Done.md
- docs/30-architecture/Repo-Index.md updated

### BE-020 Capture Policy endpoint (merged PR #8)
- Auth-protected GET /capture-policy/{mode}
- mode=corrosion → fixed “interim MVP defaults”
- mode=osmosis → 404 POLICY_NOT_DEFINED
- invalid mode → 422
- Tests: tests/test_capture_policy.py (includes unique email fix); CI green

## Current Test/CI Status
- Tests: tests/test_auth_smoke.py, tests/test_capture_policy.py
- CI: GitHub Actions running automatically; status green at baseline

## Open / Deferred Items
### Critical technical debt: Global store issue
Root cause is “global store” design. Worked around in tests for now, but will likely cause pain as tests grow.

**Proposed ticket:** BE-0xx: app.state user_store + dependency injection refactor  
**Note:** Do not include this in PR #8 scope (already not included).

### Capture Policy scope intentionally minimal
Osmosis returns 404 POLICY_NOT_DEFINED; corrosion defaults are fixed.
Next: align endpoint with API-Spec/ADR and define versioning approach.

### Optional CI hardening (not urgent)
Matrix (py 3.11/3.12), cache, lint/format, etc. Current target “smoke” is met.
