# ADR-0002: No omni-merge across users/apps in Phase-1

## Status
Accepted

## Context
Multiple users (e.g., captain and owner) may run the app separately and perform osmosis/corrosion capture flows for the same physical yacht. A question emerged whether Phase-1 should merge these observations into a unified yacht history ("omni-merge").

## Decision
Phase-1 will NOT implement omni-merge across separate app instances/users.
Each app instance only owns its own captured records.

## Consequences
- Phase-1 scope remains small and testable.
- No cross-user conflict resolution, no shared yacht identity graph, no data-sharing permissions in Phase-1.
- A future Phase-2 epic may introduce shared yacht identity + access control + merge semantics.
