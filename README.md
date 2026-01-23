# maretechapp
Maretech is a mobile app that helps boat owners detect and track visual signals related to Osmosis and Corrosion over time. It is NOT a survey tool and does NOT provide binding diagnoses.

This repo is the initial source-of-truth structure (Context Pack, ADR, Protocol)

# Maretech App — Start Here

## Read first (source of truth)
1) /docs/00-context/Context-Pack.md
2) /adr/ (decision log)
3) /docs/20-ux/App-Map.md

What to open depending on your question

Repo navigation (recommended):
/docs/30-architecture/Repo-Index.md

Product scope:
- Planned: /docs/10-product/PRD.md (not in repo yet)

Pricing:
- Planned: /docs/10-product/Pricing.md (not in repo yet)

UX: /docs/20-ux/*
Architecture: /docs/30-architecture/*
AI: /docs/40-ai/*
API: /docs/50-api/API-Spec.md
Delivery plan: /docs/60-delivery/*

## Working protocol
See: /docs/00-context/Operating-Protocol.md

## Current status
- MVP: in definition
- Next docs to produce: Repo skeleton templates

## Backend Quickstart (BE-010)

### Requirements

- Python 3.11+
- `MARETECH_JWT_SECRET` is REQUIRED (app will fail fast without it)

### Environment

Set these env vars before running:

- `MARETECH_JWT_SECRET` (required)
- `MARETECH_PASSWORD_SALT` (recommended; defaults to `dev-salt` if not set)

**Example (bash):**
```bash
export MARETECH_JWT_SECRET="change-me"
export MARETECH_PASSWORD_SALT="change-me-too"
```

### Install & Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Run Tests
```bash
pytest -q
```
