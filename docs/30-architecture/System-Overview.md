# System Overview — Maretech Mobile App
Version: v1.0
Status: Architecture baseline (MVP)

## 1) High-Level Architecture

Maretech follows an **async, event-driven architecture** optimized for:
- minimal backend coupling
- scalable AI inference
- non-blocking mobile UX

Core principle:
> Mobile triggers jobs. Backend processes. Results are pulled, not pushed.

---

## 2) Main Components

### 2.1 Mobile App
Responsibilities:
- User onboarding & mode selection (Osmosis / Corrosion)
- Guided photo capture
- Quality checks (client-side)
- Upload initiation
- Result visualization
- Timeline / comparison (corrosion only, paid)

Mobile app NEVER:
- Runs AI inference
- Makes diagnostic claims
- Stores raw AI logic

---

### 2.2 API Gateway
Responsibilities:
- Authentication
- Inspection lifecycle management
- Presigned upload URL generation
- Payment validation hooks
- Result retrieval

Stateless by design.

---

### 2.3 Object Storage
- Stores uploaded images
- Stores processed artifacts (thumbnails, masks, etc.)
- Accessed via presigned URLs only

No direct public access.

---

### 2.4 Job Queue
- Each inspection creates a job
- Jobs are mode-specific:
  - OsmosisJob
  - CorrosionJob
- Ensures:
  - async execution
  - retry logic
  - idempotency

---

### 2.5 AI Inference Service
Responsibilities:
- Pull images from storage
- Run visual analysis
- Produce:
  - signal detection
  - confidence score
  - explanation tokens (not text yet)

Inference service is:
- isolated
- replaceable
- non-user-facing

---

### 2.6 Result Store
Stores:
- inspection metadata
- mode
- confidence levels
- derived signals
- timestamps

Used by:
- result screen
- timeline
- comparison views

---

## 3) End-to-End Flow

### 3.1 Inspection Creation
1. User selects mode
2. App requests inspection session
3. Backend returns inspection_id + upload URLs

### 3.2 Capture & Upload
4. User captures photos
5. Photos uploaded directly to storage
6. Backend notified of completion

### 3.3 Processing
7. Job queued
8. AI inference runs async
9. Results stored

### 3.4 Result Consumption
10. App polls for result
11. Result displayed
12. (Corrosion only) timeline updated

---

## 4) Mode Isolation (Critical)

- Osmosis and Corrosion:
  - separate job types
  - separate confidence logic
  - separate wording rules
- Shared infrastructure, **not shared semantics**

No unified “inspection” logic at interpretation level.

---

## 5) Payment & Access Control

### Osmosis
- Payment required before job creation
- One inspection = one payment
- No subscription logic

### Corrosion
- First inspection free
- Tracking / compare locked behind subscription
- Subscription validated at API layer

---

## 6) Async & Safety Principles

- All AI processing is async
- Mobile UI must never block on inference
- Job processing must be idempotent
- Payment webhooks must be replay-safe

---

## 7) Explicit Non-Goals (MVP)

- Real-time inference
- Offline AI processing
- Sensor ingestion
- Marina-wide dashboards
- Regulatory compliance reporting
