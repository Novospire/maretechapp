# Context Pack — Maretech App (Source of Truth)
Version: v1.1  
Last updated: 2026-01-20

## 1) Product in one sentence
Maretech is a mobile app for boat owners that detects and tracks **visual signals** related to **Osmosis** and **Corrosion** over time.
It is **NOT** a survey tool and does **NOT** provide binding diagnoses.

## 2) What this product is (and is not)
### It is
- A guided photo-capture workflow (standardization)
- Visual signal analysis with confidence levels
- Repeatable tracking and comparisons over time (memory + trend)
- A decision-support tool for “should I monitor / should I escalate to survey?”

### It is not
- A diagnostic medical-style tool for boats
- A replacement for professional surveyor inspections
- A legally binding report generator
- A marina/pier operator platform for MVP

## 3) Non-negotiable decisions (fixed)
- Osmosis and Corrosion are **TWO SEPARATE PRODUCTS** under **ONE app shell**.
- Each product has separate: onboarding, positioning, pricing, and analysis language.
- Osmosis: first inspection is **PAID** (no free entry).
- Corrosion: first inspection is **FREE**; tracking/history/compare is **PAID** (subscription).
- No discounts for 2nd/3rd Osmosis inspections (pricing remains consistent).
- We sell **consistency + memory + trend**, not “AI sees better than humans”.

## 4) Target users & non-targets
### Primary (MVP)
- Private boat owners
- Captains / crew (operational users)

### Secondary (later)
- Brokers / pre-sale checks (non-binding)

### Out of scope (for MVP)
- Marina / pier operators as primary buyers
- Any workflow requiring marina staff to perform repeated measurements reliably
- Any claim that substitutes regulatory/compliance survey requirements

## 5) Core value proposition
- Standardized capture + visual analysis + repeatable comparisons
- Helps users not miss early visual signals
- Provides structured guidance + recommended re-check windows
- Turns “I’m not sure” into “monitor / recheck / escalate”

## 6) Product boundaries (legal + expectation)
- Not a diagnosis; not legally binding.
- Not a replacement for professional survey.
- We provide visual-signal analysis with confidence levels and guidance.
- Output language must remain probabilistic (signal / risk / confidence), not definitive (has/doesn’t have).

## 7) Monetization model (current)
- Osmosis: pay-per-inspection
- Corrosion: subscription to unlock tracking/history/compare + reminders

## 8) UX structure (high level)
Entry → Mode Selection

### Osmosis flow
Pay → Onboarding → Capture → Analysis → Result → Suggested follow-up

### Corrosion flow
Free 1st → Capture → Result → Offer tracking subscription → Timeline/Compare

## 9) Technical structure (high level)
Mobile → Presigned Upload → Queue → Inference → Result Store → Timeline/Compare  
- Async jobs for analysis
- Idempotency + webhook safety required (payments + inspection lifecycle)

## 10) Open questions (must be resolved later)
### Capture & model
- Minimum photo set requirements per mode (how many, which angles, quality rules)
- Confidence thresholds and wording per mode (what qualifies as SUSPECT vs CLEAR, etc.)
- Interim MVP default will be defined via capture-policy config (see ADR 0001)
- **Phase-1 note:** We do not collect passive/background location (GSM/GPS) or weather/environment data in Phase-1. Only images + optional user-entered context are used. (ADR-0003)

### Product operations
- Re-check timing logic defaults per mode (recommended windows and triggers)
- Offline vs online processing strategy (future, not MVP)
