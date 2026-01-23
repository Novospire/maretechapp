# UI Tickets — Maretech Mobile App
Version: v1.0  
Status: MVP build tickets

---

## GLOBAL RULES
- Osmosis and Corrosion flows are strictly isolated
- No mixed language, no shared result screens
- All copy is probabilistic, non-binding

---

## TICKET GROUP 0 — App Entry & Guardrails

### UI-001 Splash Screen
- App logo
- Loading state

### UI-002 Legal Disclaimer Screen
- “Not a survey”
- “Not legally binding”
- Accept & continue CTA
- Must be shown once per install

### UI-003 Authentication Gate (Required)

- Sign in (email + password)
- Create account
- Forgot password (link / code)
- Session restore (auto-login if token valid)
- Logout (in Settings)

Acceptance:
- User cannot start an inspection flow without being authenticated.
- If user launches app already authenticated, skip to Mode Selection.

---

## TICKET GROUP 1 — Mode Selection

### UI-010 Mode Selection Screen
- Two clear choices:
  - Osmosis Inspection
  - Corrosion Inspection
- Short explanatory text under each
- Selection is mandatory

---

## TICKET GROUP 2 — Osmosis Flow (Paid)

### UI-020 Osmosis Intro
- What osmosis is (high level)
- What this app does / does not do
- Clear “Paid inspection” label

### UI-021 Osmosis Payment
- Price display
- App Store / Play Store payment trigger
- Error & retry states

### UI-022 Osmosis Capture Guide
- Photo instructions
- Angle / distance hints
- “Good / Bad example” visuals (placeholder)

### UI-023 Osmosis Capture Screen
- Camera access
- Capture sequence enforcement
- Retake on quality fail

### UI-024 Osmosis Processing
- Non-blocking loading
- “Analysis in progress” message

### UI-025 Osmosis Result
- Signal detected: Yes / No / Inconclusive
- Confidence level (Low / Medium / High)
- Explanation text
- Guidance CTA (monitor / recheck / survey)

---

## TICKET GROUP 3 — Corrosion Flow (Free → Paid)

### UI-030 Corrosion Intro
- Free first inspection message
- Short explanation

### UI-031 Corrosion Capture Guide
- Same rigor as paid flow
- Capture slots are driven by “capture policy” for corrosion
- Free tier limit: up to 5 points (each point has 3 required angles)
- Explain that points > 5 require subscription

### UI-032 Corrosion Capture Screen
- Camera + quality enforcement
- Display point counter (e.g., 1/5 free)
- Enforce required angles per point (3 slots)
- If user attempts to add point 6:
  - Show paywall (UI-035)
  - Do not allow creating additional slots unless subscribed

### UI-032a Corrosion Follow-up Capture Alignment (P1)

- If a previous inspection exists:
  - Show “ghost overlay” of the corresponding photo slot from previous inspection
  - Toggle on/off
  - Opacity slider (optional)
- If no previous slot photo exists: no overlay

Acceptance:
- Overlay is only available for follow-up inspections (not first).
- Overlay never mixes modes (corrosion-only).

### UI-033 Corrosion Processing
- Async processing screen

### UI-034 Corrosion Free Result
- Signal + confidence
- Limited explanation
- NO comparison

### UI-035 Corrosion Paywall
- “Track changes over time”
- Subscription options
- Skip / Later option

---

## TICKET GROUP 4 — Corrosion Tracking (Paid)

### UI-040 Corrosion Timeline
- List of inspections
- Date + confidence

### UI-041 Corrosion Comparison
- Side-by-side view
- Trend indicator (improving / stable / worsening)

---

## TICKET GROUP 5 — Shared Screens

### UI-050 Inspection History
- Mode-filtered list
- Tap to detail

### UI-051 Inspection Detail
- Photos used
- Summary
- Confidence explanation

### UI-052 Settings
- Account
- Subscription status
- Legal text
