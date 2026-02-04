# BE-0xz: Capture metadata (minimal) stored per capture event

## Problem
We need capture context (device/app/env) to debug quality and reduce false positives without implementing device calibration.

## Decision (Phase-1.5)
Add minimal capture metadata fields to request/record model and persist them alongside capture events.

## Scope
1) schemas: add CaptureMeta (minimal)
   - device_model (str, optional)
   - os_name (str, optional)  # ios/android
   - os_version (str, optional)
   - app_version (str, optional)
   - captured_at (datetime, optional)
2) endpoint: accept metadata in capture request payload (optional)
3) storage: persist metadata with capture record (in-memory / placeholder if DB not present yet)
4) tests: ensure endpoint accepts payload with/without metadata

## Non-scope
- EXIF parsing
- device allowlist/blocklist
- calibration profiles
- cross-user merge

## Acceptance Criteria
- Existing clients work unchanged (metadata optional)
- Tests cover both cases
- CI green
