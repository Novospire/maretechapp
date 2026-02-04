# BE-0xy: Capture standards (MVP) for camera + metadata (no device calibration)

## Problem
Camera capture varies by device (iOS/Android), model, lens, exposure, stabilization. We need consistent inputs for non-binding detection without implementing full device calibration.

## Decision (MVP)
- No per-device calibration, no lens profile calibration in Phase-1.
- Implement "Capture Standards" + "User Guide" + "Capture metadata logging".

## Scope (Phase-1)
1) Define capture constraints returned by /capture-policy (min resolution, lighting, distance hints, orientation, stability hints).
2) Collect capture metadata per capture event (device model, OS, app version, timestamp; optional EXIF if available).
3) Add a minimal "capture quality checks" layer (non-blocking):
   - Reject if resolution below minimum
   - Warn if image too dark / blurry (basic heuristic only)
4) Docs: create a capture guide for users.

## Non-scope (explicit)
- No camera intrinsics calibration
- No device model allowlist/blocklist enforcement (unless later needed)
- No cross-user merge / shared yacht identity
- No hard "diagnosis" language

## Acceptance Criteria
- /capture-policy documents capture constraints for corrosion; osmosis may remain 404 until defined.
- New schema/model can store capture metadata.
- Tests cover policy + metadata presence.
- CI remains green.
