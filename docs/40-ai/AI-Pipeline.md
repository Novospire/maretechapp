# AI Pipeline — Maretech Mobile App

**Version:** v1.0  
**Status:** AI baseline (MVP)

---

## 1) AI Design Philosophy

**Core principle:**

> The AI does NOT diagnose.  
> The AI detects and compares **visual signals** with confidence levels.

AI output must always be:

- probabilistic
- explainable at a high level
- non-binding

The system optimizes for:

- consistency
- repeatability
- trend detection

**Not absolute truth.**

---

## 2) Input Constraints (Critical)

AI operates ONLY on:

- user-provided images
- captured via guided workflows

AI does NOT use:

- sensor data
- metadata inference beyond time/order
- external datasets at runtime

**Garbage in = garbage out.**  
Therefore, capture quality enforcement is mandatory.

---

## 3) High-Level Pipeline
```mermaid
flowchart LR
    A[Mobile Capture] --> B[Quality Check]
    B -->|pass| C[Object Storage]
    B -->|fail| A
    C --> D[Job Queue]
    D --> E[Inference Service]
    E --> F[Signal Extraction]
    F --> G[Confidence Scoring]
    G --> H[Result Structuring]
    H --> I[Result Store]
    I --> J[Mobile Result View]
```

---

## 4) Pipeline Stages

### 4.1 Capture & Quality Check

- Angle consistency
- Focus / blur
- Lighting sufficiency
- Surface coverage

**Failing inputs are rejected before upload.**

### 4.2 Job Creation

- One job per inspection
- Job is immutable once queued
- Job type:
  - `OsmosisJob`
  - `CorrosionJob`

### 4.3 Inference

- Visual feature extraction
- Pattern recognition
- No hard classification labels exposed to user

**Raw model outputs are never user-facing.**

### 4.4 Signal Extraction

Signals may include (non-exhaustive):

- discoloration patterns
- blister-like formations
- surface irregularities
- texture deviations

**Signals are mode-specific.**

### 4.5 Confidence Scoring

Confidence is derived from:

- signal strength
- signal consistency across images
- model certainty thresholds

Confidence levels:

- Low
- Medium
- High

**No numeric probabilities shown in MVP.**

### 4.6 Result Structuring

Results are converted into:

- human-readable summaries
- mode-specific wording
- guidance suggestions:
  - monitor
  - re-check
  - escalate

**Language rules differ per mode.**

---

## 5) Mode-Specific Logic

### Osmosis

- Conservative thresholds
- Higher uncertainty tolerance
- Language favors escalation if confidence is Medium+

### Corrosion

- Comparative logic enabled
- Trend-based interpretation:
  - worsening
  - stable
  - improving
- Timeline-aware confidence adjustments

---

## 6) Learning & Feedback (Explicitly Limited)

**MVP constraints:**

- No continuous online learning
- No user feedback loop into model training
- Model updates are manual and versioned

**This avoids silent behavior changes.**

---

## 7) Failure & Fallback Rules

**If AI fails:**

- Result marked as `Inconclusive`
- User informed clearly
- No forced upsell or misleading output

---

## 8) Explicit Non-Goals (MVP)

- Predictive corrosion modeling
- Structural integrity estimation
- Regulatory compliance scoring
- Cross-vessel benchmarking

---
