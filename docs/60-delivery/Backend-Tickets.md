# Backend Tickets — Maretech App
Version: v1.0  
Status: MVP backend implementation plan

---

## GLOBAL RULES
- Mode isolation is enforced at data + wording level
- AI is async only (never block request threads)
- Idempotency for create/complete flows
- Store `model_version` with every result

---

## BE-000 Setup & Skeleton
- Create backend project scaffold
- Health check endpoint
- Env var handling
- Basic logging

Acceptance:
- Server runs locally
- /health returns ok

---

## BE-010 Auth Middleware (JWT)
- Validate bearer token
- Attach user_id to request context

Acceptance:
- Protected routes reject missing/invalid tokens

---

## BE-020 Create Inspection Session
Implements: POST /inspections

- Validate mode
- Enforce osmosis payment requirement (gate via payment status flag)
- Create inspection record
- Generate presigned upload URLs

Acceptance:
- Returns inspection_id + upload_urls + expires_at
- Mode cannot be changed after creation

---

## BE-030 Complete Upload
Implements: POST /inspections/{id}/complete

- Validate inspection exists + belongs to user
- Mark upload complete
- Enqueue job (osmosis or corrosion)

Acceptance:
- Returns status: queued
- Idempotent: repeated calls do not create duplicate jobs

---

## BE-040 Get Inspection Status
Implements: GET /inspections/{id}

- pending / processing / completed / failed

Acceptance:
- Status reflects job state transitions

---

## BE-050 Get Inspection Result
Implements: GET /inspections/{id}/result

- Only returns when completed
- Includes confidence_level, signal_detected, guidance, model_version

Acceptance:
- Contract matches API-Spec.md

---

## BE-060 Inference Stub Worker (MVP)
- Implement worker that consumes queued jobs
- For now: produce deterministic mocked outputs per mode
- Persist result to result store

Acceptance:
- End-to-end flow works without real AI

---

## BE-070 Payments Validate (Osmosis)
Implements: POST /payments/validate

- Receipt payload accepted
- For MVP: mock validation
- Persist payment status against user/session

Acceptance:
- Osmosis inspection creation is blocked unless payment valid

---

## BE-080 Subscriptions Status (Corrosion)
Implements: GET /subscriptions/status

- Returns active plan
- For MVP: mock subscription state

Acceptance:
- Corrosion tracking endpoints are blocked unless active=true

---

## BE-090 Corrosion History
Implements: GET /corrosion/history

- Returns inspections list
- Requires active subscription

Acceptance:
- Non-subscribed users get 403

---

## BE-100 Corrosion Compare
Implements: GET /corrosion/compare?from=&to=

- Validate both inspections belong to user and are corrosion
- Return derived trend (improving/stable/worsening)

Acceptance:
- Returns trend string
- 400 on invalid ids/mode mismatch

---

## BE-110 Error Handling Standard
- Standard error response format
- Map common errors (401/403/404/400/500)

Acceptance:
- Errors match API-Spec.md shape
