# Model Inputs & Outputs — Maretech Mobile App

**Version:** v1.0  
**Status:** AI I/O baseline (MVP)

---

## 1) Purpose & Scope

This document defines:

- What the AI model **accepts** as input
- What the AI model **produces** as output
- What is **persisted** vs **derived**
- Mode-specific differences (Osmosis vs Corrosion)

**This is NOT an API spec.**

It is the canonical contract between:

- Mobile App
- Backend Services
- AI Inference Service

---

## 2) High-Level Contract

### Inputs

- Images + minimal inspection context
- Provided **only** after quality checks pass

### Outputs

- Visual signal summary
- Confidence level
- Mode-specific guidance tokens

**No raw model tensors or probabilities are exposed to users.**

---

## 3) Input Schema (to Inference Service)

### 3.1 Inspection Context
```json
{
  "inspection_id": "uuid",
  "mode": "osmosis | corrosion",
  "created_at": "ISO-8601",
  "model_version": "string"
}
```

**Constraints:**

- `mode` is immutable once job is queued
- `model_version` is required for reproducibility

### 3.2 Image Payload
```json
{
  "images": [
    {
      "image_id": "uuid",
      "object_storage_url": "presigned-url",
      "capture_order": 1,
      "angle_hint": "string | null"
    }
  ]
}
```

**Rules:**

- Images are already validated for quality
- Order matters
- No EXIF-based inference allowed in MVP

---

## 4) Output Schema (from Inference Service)

### 4.1 Core Result
```json
{
  "inspection_id": "uuid",
  "mode": "osmosis | corrosion",
  "signal_detected": "yes | no | inconclusive",
  "confidence_level": "low | medium | high"
}
```

**Rules:**

- `signal_detected` is not a diagnosis
- `confidence_level` is categorical (no numbers)

### 4.2 Signal Details (Internal / Non-User-Facing)
```json
{
  "signals": [
    {
      "type": "string",
      "strength": "weak | moderate | strong"
    }
  ]
}
```

**Notes:**

- Stored internally for auditing and future model analysis
- Not shown directly to users in MVP

### 4.3 Guidance Tokens
```json
{
  "guidance": [
    "monitor",
    "recheck_later",
    "consider_professional_survey"
  ]
}
```

**Rules:**

- Guidance tokens are mapped to user-facing language at app layer
- Tokens differ per mode

---

## 5) Mode-Specific Output Rules

### 5.1 Osmosis

- `signal_detected = inconclusive` allowed and common
- Conservative confidence thresholds
- Guidance favors escalation if confidence >= medium

**Example:**
```json
{
  "signal_detected": "yes",
  "confidence_level": "medium",
  "guidance": ["consider_professional_survey"]
}
```

### 5.2 Corrosion

- Comparative logic enabled (if historical data exists)
- Guidance may include trend language (derived, not model output)

**Example:**
```json
{
  "signal_detected": "yes",
  "confidence_level": "high",
  "guidance": ["monitor", "recheck_later"]
}
```

---

## 6) Persisted vs Derived Data

### Persisted

- `inspection_id`
- `mode`
- timestamps
- `confidence_level`
- `signal_detected`
- `model_version`

### Derived (at app/backend layer)

- Trend status (improving / stable / worsening)
- Comparison visuals
- Reminder scheduling

---

## 7) Failure & Fallback Payload

**If inference fails:**
```json
{
  "inspection_id": "uuid",
  "signal_detected": "inconclusive",
  "confidence_level": "low",
  "guidance": ["recheck_later"]
}
```

**Rules:**

- Failure is explicit
- No silent degradation
- No forced upsell

---

## 8) Versioning Rules

- Every model update increments `model_version`
- Historical inspections remain tied to original model version
- No retroactive reinterpretation of past results

---

## 9) Explicit Non-Goals (MVP)

- Numeric probability exposure
- Multi-modal inputs (sensor + image)
- Cross-vessel normalization
- Predictive time-to-failure estimation

---
