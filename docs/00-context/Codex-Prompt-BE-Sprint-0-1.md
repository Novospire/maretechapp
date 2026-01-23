# Codex Prompt — Backend Sprint 0/1 (v1.0)
Repo: Novospire/maretechapp
Baseline: main@HEAD

You MUST follow repo docs as source of truth:
- /docs/00-context/Context-Pack.md
- /adr/0001-capture-policy.md
- /docs/20-ux/UI-Tickets.md (UI-035 acceptance criteria)

Non-negotiables:
- Osmosis and Corrosion are isolated (no mixed endpoints, no mixed schemas)
- No diagnosis; outputs are non-binding
- Async-only inference (never block request waiting for model)
- Enforce UI-035 rules server-side via entitlements

Implement ONLY tickets defined in:
- /docs/30-architecture/Backend-Sprint-0-1.md

Deliverables:
1) FastAPI project skeleton (app, routers, schemas, services)
2) Postgres models + migrations (minimal)
3) Celery worker + Redis broker + status polling
4) Entitlement checks for osmosis payment mock and corrosion subscription mock
5) API docs via OpenAPI

Forbidden:
- No UI work
- No new product scope
- No synchronous inference
