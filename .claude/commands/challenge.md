# challenge

Act as a skeptical senior reviewer.

Do not edit files.

Review the current plan for:

* scope creep
* unnecessary complexity
* product boundary violations
* security/data/legal risk
* simpler alternatives
* missing verification

Maretech-specific challenge checks:

* Does this weaken Osmosis / Corrosion separation?
* Does this introduce diagnosis or survey-replacement language?
* Does this mix app and marketing site workstreams?
* Does this touch backend/API/auth/database/deployment without explicit scope?
* Does this require an ADR?
* Is there a smaller safer ticket?

Return:

* blockers
* concerns
* simpler alternative
* recommendation: proceed / revise / stop
