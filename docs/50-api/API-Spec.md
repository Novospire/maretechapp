# API Specification — Maretech Mobile App

**Version:** v1.0  
**Status:** API baseline (MVP)

---

## 1) Principles

- REST over HTTPS
- JSON only
- Async-first (AI inference is never blocking)
- Idempotent operations where applicable
- Strict mode isolation (osmosis ≠ corrosion)

**Base URL:**
```
https://api.maretech.app/v1
```

---

## 2) Authentication

### 2.1 Auth Method

- Bearer token (JWT)
- Token issued after app login/signup

**Header:**
```
Authorization: Bearer <token>
```

---

## 3) Inspection Lifecycle

### 3.1 Create Inspection Session

Creates an inspection container and returns upload URLs.

**`POST`** `/inspections`

**Request:**
```json
{
  "mode": "osmosis | corrosion"
}
```

**Rules:**

- `mode` is required and immutable
- Osmosis requires valid payment before creation

**Response:**
```json
{
  "inspection_id": "uuid",
  "upload_urls": ["presigned-url-1", "presigned-url-2"],
  "expires_at": "ISO-8601"
}
```

### 3.2 Complete Upload

Signals backend that uploads are finished.

**`POST`** `/inspections/{inspection_id}/complete`

**Response:**
```json
{
  "status": "queued"
}
```

### 3.3 Get Inspection Status

Polls inspection progress.

**`GET`** `/inspections/{inspection_id}`

**Response:**
```json
{
  "inspection_id": "uuid",
  "status": "pending | processing | completed | failed"
}
```

### 3.4 Get Inspection Result

Returns structured result (if completed).

**`GET`** `/inspections/{inspection_id}/result`

**Response:**
```json
{
  "inspection_id": "uuid",
  "mode": "osmosis | corrosion",
  "signal_detected": "yes | no | inconclusive",
  "confidence_level": "low | medium | high",
  "guidance": ["monitor", "recheck_later"],
  "model_version": "string",
  "created_at": "ISO-8601"
}
```

---

## 4) Corrosion-Specific APIs

### 4.1 Inspection History

Requires active subscription.

**`GET`** `/corrosion/history`

**Response:**
```json
{
  "inspections": [
    {
      "inspection_id": "uuid",
      "created_at": "ISO-8601",
      "confidence_level": "medium"
    }
  ]
}
```

### 4.2 Comparison View

Returns two inspections for side-by-side comparison.

**`GET`** `/corrosion/compare?from={id}&to={id}`

**Response:**
```json
{
  "from": "inspection_id",
  "to": "inspection_id",
  "trend": "improving | stable | worsening"
}
```

---

## 5) Payments

### 5.1 Osmosis Payment Validation

Payment must be confirmed before inspection creation.

**`POST`** `/payments/validate`

**Request:**
```json
{
  "provider": "app_store | play_store",
  "receipt": "string"
}
```

**Response:**
```json
{
  "status": "valid | invalid"
}
```

---

## 6) Subscriptions (Corrosion)

### 6.1 Subscription Status

**`GET`** `/subscriptions/status`

**Response:**
```json
{
  "active": true,
  "plan": "monthly | yearly"
}
```

---

## 7) Idempotency & Safety

- `POST /inspections` must be idempotent per user + mode + timestamp window
- Duplicate uploads are ignored
- Job execution is retry-safe

---

## 8) Error Handling

**Standard error format:**
```json
{
  "error_code": "string",
  "message": "human readable explanation"
}
```

---

## 9) Explicit Non-Goals (MVP)

- Webhooks to third parties
- Real-time streaming updates
- Public or shareable inspection URLs
- Bulk inspection APIs

---
