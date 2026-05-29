# Contributing

## Working Rule

Use repository files as source of truth.

Do not rely on chat history as source of truth.

## Branching

Never commit directly to main.

Use:

branch → PR → review → squash merge

## Scope

One PR should cover one small ticket.

Do not mix:

* docs
* backend
* API
* auth
* database
* deployment
* mobile UI
* marketing site UI

unless explicitly approved.

## Local Artifacts

Do not commit:

* .env files
* secrets
* **pycache**
* node_modules
* build outputs
* local backup files
* generated artifacts

## Maretech Product Boundaries

* Maretech is not a survey tool.
* Maretech does not provide binding diagnoses.
* Osmosis and Corrosion are separate products under one app shell.
* Output language must remain probabilistic.
* App and marketing site workstreams must stay separate.

## Pull Requests

Every PR must include:

* why
* scope
* non-scope
* changed files
* verification
* known warnings / non-blockers

## Done Means

Done requires evidence:

* changed files list
* diff summary
* verification output
* no forbidden files changed
* no generated/local files committed
