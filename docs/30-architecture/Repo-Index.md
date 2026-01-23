# Repo Index — Maretech App
Version: v1.0
Status: Start-here (source-of-truth navigation)

## 0) Non-negotiable source of truth
- /docs/00-context/Context-Pack.md
- /docs/00-context/Operating-Protocol.md
- /adr/ (decision log)

## 1) Current sprint execution (Codex entry)
- /docs/30-architecture/Backend-Sprint-0-1.md
- /docs/00-context/Codex-Prompt-BE-Sprint-0-1.md

## 2) UX (current baseline)
- /docs/20-ux/App-Map.md
- /docs/20-ux/UI-Tickets.md

## 3) API contract
- /docs/50-api/API-Spec.md

## 4) Planned / not in repo yet (do not treat as truth)
- /docs/30-architecture/System-Overview.md
- /docs/40-ai/AI-Pipeline.md
- /docs/60-delivery/Sprint-Backlog.md
- /docs/10-product/PRD.md
- /docs/10-product/Pricing.md

## Operating rule (agents)
When asking an agent (Codex/Claude) to implement features:
1) Provide BASELINE: main@HEAD
2) Provide the exact file list from sections 0–3 above (only)
3) Provide the current ticket IDs and acceptance criteria
4) Require small PRs; no scope expansion
