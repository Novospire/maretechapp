# Operating Protocol (Source of Truth)

## Golden Rule
We do not rely on chat history as source of truth.
The source of truth is:
1) /docs/00-context/Context-Pack.md
2) /adr/*
3) README.md (index)

## How to work with ChatGPT
For every new chat:
- Provide repo URL once
- Provide paths of changed docs
- Paste the changed sections or a short diff (20-60 lines)

## Change Management
Any decision that changes scope, pricing model, product separation, legal stance, or architecture MUST be captured as an ADR.
Then Context-Pack must be updated.

## What goes where
- "What is true right now?" -> Context-Pack
- "Why did we choose this?" -> ADR
- "What will we build?" -> PRD + App-Map + API-Spec
- "How does it work technically?" -> System-Overview + AI-Pipeline + Data-Model
- "When will we deliver?" -> Phases + Sprint-Backlog

## Definition of Decision
A decision is something that is:
- Hard to reverse
- Impacts product scope or monetization
- Impacts legal positioning
- Impacts architecture or data model
