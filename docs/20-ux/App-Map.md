# App Map — Maretech Mobile App
Version: v1.0
Status: Draft (UX baseline)

## 1) Entry & Global Structure

### App Entry
- Splash
- Legal disclaimer (non-binding, not a survey)
- Continue

### Mode Selection (Critical Fork)
User must explicitly choose ONE mode:
- Osmosis Inspection
- Corrosion Inspection

> Modes are isolated.  
> User never sees mixed language, mixed results, or mixed flows.

---

## 2) Osmosis Flow (Paid-first)

### Osmosis — Entry
- Short explanation:
  - What osmosis is (high level)
  - What this app does / does not do
- Clear disclaimer (visual signals only)
- Price shown upfront

### Payment
- One-time payment (per inspection)
- Payment required to proceed

### Osmosis Onboarding
- What to photograph
- Where to photograph
- What quality is required
- “This is NOT a diagnosis” reminder

### Capture Flow
- Guided photo capture
- Angle / distance / area guidance
- Retake enforcement if quality fails

### Analysis
- Upload
- Async processing
- Progress indicator (non-blocking)

### Result Screen
- Signal detected: Yes / No / Uncertain
- Confidence level (low / medium / high)
- Plain-language explanation
- Recommendation:
  - Monitor
  - Re-check later
  - Consider professional survey

### Post-Result
- No free comparisons
- No discounts for future inspections
- CTA: “Run another inspection” (paid)

---

## 3) Corrosion Flow (Free entry → Paid tracking)

### Corrosion — Entry
- Short explanation
- Clear “free first inspection” message
- Disclaimer

### First Capture (Free)
- Guided capture (same rigor as paid)
- Quality enforcement

### Analysis
- Upload
- Async processing

### First Result (Free)
- Signal presence
- Confidence level
- Basic explanation
- NO timeline / NO compare

### Paywall Moment (Critical)
User sees:
- “Track changes over time”
- “Compare past inspections”
- “Get reminders”

Subscription options displayed.

### Subscription
- Monthly / yearly (details later)
- Unlocks tracking features

### Tracking Mode
- Timeline view
- Comparison view (side-by-side)
- Trend indicators (improving / stable / worsening)

---

## 4) Shared Screens (Both Modes)

### Inspection History
- List of inspections (mode-isolated)
- Date, location (if allowed), confidence

### Inspection Detail
- Photos used
- Analysis summary
- Confidence explanation

### Settings
- Legal disclaimers
- Data usage
- Account / subscription

---

## 5) Explicit UX Constraints (Non-negotiable)

- Osmosis and Corrosion NEVER share:
  - Result screens
  - Confidence wording
  - Recommendations
- No “combined report”
- No “overall boat health score”
- Language must remain probabilistic

---

## 6) Out of Scope (Explicitly)
- Marina dashboards
- Staff workflows
- Sensor integrations
- Offline analysis (future)
