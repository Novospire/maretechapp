# Backend Sprint 0/1 — Ticket Map (v1.0)
Baseline: main@HEAD

## Goals (locked)
- Auth gate before inspections
- Mode isolation: Osmosis and Corrosion are isolated
- Async-only inference (no blocking calls)
- Non-binding outputs (NOT a diagnosis)

## Core Entities (minimum)
- User
- Inspection (mode: osmosis|corrosion, status)
- CaptureSlot (inspection_id, slot_index/point_index, required_angles)
- MediaAsset (slot_id, angle_id, uri, quality_meta)
- InferenceJob (inspection_id, celery_task_id, state)
- Result (inspection_id, mode-specific payload, confidence, explanation)
- Entitlement (user_id, corrosion_free_used, corrosion_points_allowed, subscription_active mock, osmosis_payments mock)

## BE Tickets
### BE-010 Auth (Required)
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- GET  /auth/me (session restore)
Acceptance:
- All inspection endpoints require auth

### BE-020 Capture Policy (ADR-0001 aligned)
- GET /capture-policy/{mode}
Acceptance:
- Returns interim MVP defaults (corrosion: 5 points free, 3 angles/point; paid up to 10 points)

### BE-030 Inspection Lifecycle
- POST /inspections (mode required)
- GET  /inspections?mode=
- GET  /inspections/{id}
Acceptance:
- Mode filter enforced (no cross-mode leakage)

### BE-040 Upload Flow (minimal)
- POST /inspections/{id}/slots (create slot/point)
- POST /slots/{slot_id}/assets (register asset upload)
Acceptance:
- Slot creation beyond free allowance triggers entitlement failure (see BE-080)

### BE-050 Async Inference
- POST /inspections/{id}/submit (enqueue)
- GET  /inspections/{id}/status (poll)
Acceptance:
- Submit returns job id immediately (no blocking)
- Status exposes queued/running/succeeded/failed

### BE-060 Results (mode-specific)
- GET /inspections/{id}/result
Acceptance:
- Payloads are mode-isolated; corrosion does not return osmosis fields (and vice versa)

### BE-070 Payments Mock (Osmosis paid-first)
- GET /entitlements/osmosis (mock state)
- POST /payments/osmosis/mock (toggle paid for testing)
Acceptance:
- Osmosis inspection submit is blocked unless paid flag true

### BE-080 Subscription Mock (Corrosion tracking + point>5 paywall)
- GET /entitlements/corrosion (includes free allowance + subscription_active mock)
- POST /subscriptions/corrosion/mock (toggle subscribed)
Acceptance:
- Free allowance: up to 5 points/slots
- Attempt to create point 6+ returns 402/403 with reason = PAYWALL_UI_035
- After subscription_active=true, allow points up to policy max (10)
