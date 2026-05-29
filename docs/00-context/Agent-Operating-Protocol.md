# Agent Operating Protocol — Maretech

## Purpose

This file defines how AI coding tools should operate inside the Maretech repo.

Maretech uses the general AI Delivery Operating Protocol, but this file contains only Maretech-specific rules.

## Tool Roles

ChatGPT / Summer:

* product strategy
* scope control
* ticket writing
* prompt writing
* legal/risk language review
* final decision gate

Claude Code:

* backend implementation
* debugging
* refactor
* terminal/log-based investigation
* tests and verification

Codex:

* implementation support
* PR review
* architecture second opinion
* scope creep detection

Antigravity:

* UI/layout work
* visual iteration
* marketing site design exploration
* screenshot-based frontend refinement

NotebookLM / MCP / RAG:

* research/PDF/literature workflows only
* not repo source of truth

## Basic Workflow

Use for:

* docs-only changes
* small copy edits
* simple UI text adjustments
* small visual/layout changes with limited files

## Detailed Workflow

Use for:

* backend/API work
* auth
* database
* migrations
* AI output wording
* pricing
* onboarding
* deployment
* app/site architecture
* legal or risk-sensitive language

## Challenge Required When

Use a challenge/review pass before implementation when a task touches:

* AI output wording
* diagnosis-like language
* legal disclaimer
* Osmosis / Corrosion separation
* pricing
* onboarding
* API contracts
* database
* auth
* deployment
* production behavior

## Maretech Non-Negotiables

* Osmosis and Corrosion are separate products under one app shell.
* Do not merge their onboarding, pricing, analysis language or product flows.
* Maretech is not a survey replacement.
* Maretech does not provide binding diagnoses.
* Output language must stay probabilistic.
* Async-only inference is required.
* App and marketing site workstreams stay separate.

## Forbidden Scope By Default

Do not touch unless explicitly approved:

* app implementation files
* backend/API files
* auth files
* database files
* migration files
* deployment files
* package/dependency files
* .env files
* payment/pricing implementation
* production config

## Done Means

Done requires:

* changed files list
* diff summary
* verification output
* known warnings / non-blockers
* confirmation that no Maretech non-negotiables were violated
* confirmation that no forbidden files were changed
