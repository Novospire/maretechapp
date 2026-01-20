# Context Pack — Maretech App (Source of Truth)

## 1) Product in one sentence
Maretech is a mobile app that helps boat owners detect and track visual signals related to Osmosis and Corrosion over time.
It is NOT a survey tool and does NOT provide binding diagnoses.

## 2) Non-negotiable decisions (fixed)
- Osmosis and Corrosion are TWO SEPARATE PRODUCTS under ONE app shell.
- Each has separate onboarding, positioning, pricing, and analysis language.
- Osmosis: first inspection is PAID (no free entry).
- Corrosion: first inspection is FREE entry; tracking/history features are PAID via subscription.
- No discounts for 2nd/3rd Osmosis inspections (pricing remains consistent).
- We sell consistency + memory + trend, not “better eyes than humans”.

## 3) Target users
Primary:
- Boat owners (private)
- Captains / crew (operational users)
Secondary (later):
- Brokers / pre-sale checks (non-binding)
Out of scope:
- Marina/island/pier operators as primary buyers for MVP

## 4) Core value proposition
- Standardized capture + visual analysis + repeatable comparisons
- Helps users not miss early visual signals
- Provides structured guidance and recommended re-check windows

## 5) Product boundaries (legal + expectation)
- Not a diagnosis, not legally binding.
- Not a replacement for professional survey.
- We provide visual signal analysis with confidence levels and guidance.

## 6) Monetization model (current)
- Osmosis: pay-per-inspection
- Corrosion: subscription to unlock tracking/history/compare + reminders

## 7) UX structure (high level)
Entry -> Mode Selection
- Osmosis flow: Pay -> Onboarding -> Capture -> Analysis -> Result -> Suggested follow-up
- Corrosion flow: Free 1st -> Capture -> Result -> Offer tracking subscription -> Timeline/Compare

## 8) Technical structure (high level)
Mobile -> Presigned Upload -> Queue -> Inference -> Result store -> Timeline/Compare
Async jobs for analysis.
Idempotency + webhook safety required.

## 9) Open questions (must be resolved later)
- Minimum photo set requirements per mode
- Confidence scoring thresholds per mode
- Offline vs online processing (future)
