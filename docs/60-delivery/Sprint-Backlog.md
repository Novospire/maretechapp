# Sprint Backlog — Maretech App
Version: v1.0
Status: MVP execution plan

## Sprint 0 — Project Setup & Guardrails
Goal: Build can start without rework.

- Repo structure finalized
- Environments defined (dev / prod)
- Auth strategy confirmed (JWT)
- Storage bucket + presigned upload flow defined
- Legal disclaimer text (draft)

Deliverable:
- Running backend skeleton
- Empty mobile shell
- CI checks passing

## Sprint 1 — Inspection Core (Shared)
Goal: One inspection can be created, uploaded, queued, and completed.

Backend:
- POST /inspections
- POST /inspections/{id}/complete
- GET /inspections/{id}
- Job queue integration (mock inference)

Mobile:
- Mode selection screen
- Capture flow (quality checks enforced)
- Upload via presigned URLs
- Status polling

Deliverable:
- End-to-end inspection lifecycle (no AI yet)

### Planned (Sprint 1.x / Phase-1.5)
- BE-0xz Capture metadata (minimal) — status: planned

## Sprint 2 — Osmosis (Paid Flow)
Goal: Paid osmosis inspection works end-to-end.

Backend:
- Payment validation endpoint
- Osmosis job type
- Result storage

Mobile:
- Osmosis onboarding
- Paywall + payment
- Result screen (no comparison)

AI:
- Osmosis inference stub → real model

Deliverable:
- One paid osmosis inspection producing result

## Sprint 3 — Corrosion (Free + Subscription)
Goal: Corrosion flow with tracking gate.

Backend:
- Subscription status endpoint
- Corrosion job type
- History endpoint

Mobile:
- Free first corrosion inspection
- Subscription upsell screen
- Timeline view (basic)

AI:
- Corrosion inference stub → real model

Deliverable:
- Free corrosion result
- Paid tracking unlocked

## Sprint 4 — Comparison & Trend
Goal: Show value of “memory + trend”.

Backend:
- Compare endpoint
- Trend derivation logic

Mobile:
- Side-by-side comparison UI
- Trend indicators (improving / stable / worsening)

Deliverable:
- Visual comparison experience

## Sprint 5 — Hardening & Release Prep
Goal: Ship-ready MVP.

- Error handling & fallback states
- Inconclusive flows
- Copy & wording review (legal-safe)
- Performance & retry tests
- App store prep

Deliverable:
- MVP ready for limited release
