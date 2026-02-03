# BE-0xx: app.state user_store + dependency injection refactor

## Problem
Current design uses a global store / singleton-like state for user_store (and related auth state), which risks cross-test contamination and flaky behavior as test suite grows.

## Goal
Make app state (user_store) instance-scoped and injectable so each test/request context can run isolated.

## Non-goals
- No new features
- No API changes (unless strictly required for DI)
- No scope expansion beyond fixing state isolation

## Acceptance Criteria (must pass)
1) No cross-test contamination:
   - Running tests in random order yields the same results.
   - Running the same test file twice back-to-back yields identical results.
2) Isolated app construction:
   - App can be created via an app factory (or equivalent) with injected user_store.
   - Tests can provide a fresh user_store per test (fixture).
3) No global singleton dependency:
   - user_store is not imported as a global mutable singleton in request handlers.
4) CI stays green:
   - Existing tests pass unchanged or with minimal fixture updates.
   - Add at least one regression test/guard that would fail under the old global-store behavior.

## Proposed Implementation Notes (high-level)
- Introduce create_app(...) factory that accepts dependencies (user_store, config).
- Use FastAPI dependency injection or app.state to hold per-app instances.
- Update tests to build a fresh app + client per test (or per module) via fixtures.

## Files Likely Touched
- app/state.py (or current store module)
- app/main.py or app/api.py (app creation)
- app/routes/auth.py (where store is used)
- tests/conftest.py + affected tests
