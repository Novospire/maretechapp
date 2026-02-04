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

  ## Git Workflow (Source of Truth)

### Default rule

* **Never commit directly to `main`.** Always use a branch + PR.
* For docs-only changes, prefer **GitHub Web UI (PR-first)**.
* For code changes, multi-file edits, conflicts, or anything non-trivial, use **Terminal flow**.
* Merge preference: **Squash and merge** (so `main` stays clean).

  * A PR can have multiple commits; squash makes it **1 commit on `main`**.

---

## Flow A — Docs PR-first (GitHub Web UI) ✅ (default for docs)

Use this for:

* Markdown docs edits
* ADRs
* Small text updates

Steps:

1. Open the file on GitHub → click **Edit**.
2. Make changes → **Preview** → confirm formatting.
3. At the bottom (**Commit changes**):

   * Select ✅ **Create a new branch for this commit and start a pull request**
   * Branch name: `docs/<topic>` (e.g. `docs/adr-0003-references`)
   * Click **Propose changes**
4. GitHub opens the PR screen:

   * Base: `main`
   * Compare: your `docs/...` branch
   * Fill title + description → **Create pull request** (Draft optional)
5. If you need to edit more files in the same PR:

   * Edit the next file
   * In **Commit changes**, select ✅ **Commit to the existing branch** `docs/...` (NOT main)
6. Wait for checks → merge with **Squash and merge**.

Stop condition:

* If you see “Commit directly to main” selected → **STOP** and switch to branch.

---

## Flow B — Terminal branch + PR (default for code / bigger changes)

Use this for:

* Backend/frontend code changes
* Multiple files with risk
* Conflicts / refactors
* Anything requiring local tests

1. Update main

```bash
git checkout main
git pull --ff-only
```

2. Create a branch (unique name)

```bash
git checkout -b <scope>/<short-topic>
# examples:
# docs/adr-0003-references
# be/inspection-create-endpoint
# chore/ci-fix
```

3. Edit files locally, then review

```bash
git status
git diff
```

4. Stage intentionally (avoid blind `add -A` unless you really mean it)

```bash
git add <file1> <file2>
git status
```

5. Commit

```bash
git commit -m "<type>: <message>"
# examples:
# docs: reference ADR-0003 in context + capture guide
# be: inject per-app user_store (no global mutable store)
```

6. Push

```bash
git push -u origin <branch-name>
```

7. Open PR

* GitHub → **Compare & pull request** (or Pull requests → New)
* Base: `main`, Compare: `<branch-name>`
* Merge: **Squash and merge**

---

## Naming conventions

* Branch: `<area>/<topic>`

  * `docs/...`, `be/...`, `fe/...`, `chore/...`, `fix/...`
* Commit:

  * `docs: ...`
  * `be: ...`
  * `fe: ...`
  * `chore: ...`
  * `fix: ...`

---

## PR Checklist (required before merge)

**Scope & intent**

* [ ] PR title follows convention (e.g. `docs: ...`, `be: ...`)
* [ ] PR description includes:

  * [ ] **Why** (1–3 sentences)
  * [ ] **Scope** (what changed)
  * [ ] **Non-scope** (what did NOT change)
  * [ ] Links to related tickets/ADRs (if any)

**Correctness & safety**

* [ ] No direct commits to `main`.
* [ ] No scope creep (only what the ticket/decision requires).
* [ ] For Maretech: non-negotiables respected (mode isolation, no diagnosis language, async-only inference).

**Quality**

* [ ] CI checks are green.
* [ ] Tests added/updated where appropriate (at least smoke/regression if behavior changes).
* [ ] Docs updated if behavior/contract changed.

**Merge discipline**

* [ ] Merge method: **Squash and merge**.
* [ ] Delete branch after merge (unless it’s a long-running epic branch).

