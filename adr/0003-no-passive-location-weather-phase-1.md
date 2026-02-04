\# ADR-0003: No passive location/weather collection in Phase-1 (visual-first)



\## Status

Accepted



\## Context

The product is described as “visual analysis” for osmosis/corrosion. A question arose whether Phase-1 should also collect passive environment context such as GSM-based location, device location, or weather data to improve report quality.



\## Decision

Phase-1 will NOT collect passive location, GSM, or weather/environment data.



Phase-1 inputs remain:

\- Images (primary signal)

\- Optional user-provided context (manual, explicitly entered), e.g. marina/region text, approximate conditions (optional)



Any automated location/weather enrichment is deferred to Phase-2 and must be:

\- Opt-in (explicit user consent)

\- Purpose-limited and transparently disclosed

\- Optional (system must work without it)



\## Rationale

\- Privacy and trust cost outweighs potential marginal quality gains in Phase-1.

\- Passive signals can be inaccurate or misleading (stale location, VPN, offline conditions), degrading report quality.

\- Phase-1 must stay focused and testable; adding passive signals expands scope and compliance burden.



\## Consequences

\- Reports are “visual-first” with optional manual context only.

\- No background location permissions or weather API dependencies in Phase-1.

\- Phase-2 may introduce opt-in enrichment if validated by user value and compliance requirements.



\## Related

\- Context-Pack.md (inputs/assumptions)

\- Capture-Guide.md (user guidance)



