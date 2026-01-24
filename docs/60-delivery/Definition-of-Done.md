# Definition of Done (DoD) — Maretech Backend

A PR is mergeable only if:

## Scope
- [ ] Only the requested ticket(s) implemented (no extra endpoints/features)
- [ ] Out-of-scope items explicitly stated in PR description

## Repo Truth
- [ ] PR includes "Repo Read Log" (paths opened/read)
- [ ] Any REQUIRED env var change documented in README quickstart

## Quality
- [ ] Tests added/updated when behavior changes
- [ ] `pytest -q` passes locally OR CI is green
- [ ] requirements include necessary test deps if tests exist

## Delivery
- [ ] PR title matches ticket ID(s)
- [ ] PR description includes: Scope (done / not done) + Files changed summary
