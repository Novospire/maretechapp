# Done Log

## 2026-01-24
- ✅ BE-010 Auth + API skeleton — merged (PR #1) — main@HEAD: d79e6b6
- ✅ BE-012 CI smoke (pytest) — merged (PR #5) — main@HEAD: a85b371
- ✅ BE-013 Auth token uniqueness (jti) — merged (PR #6) — main@HEAD: 41c672f

## 2026-05-28
- ✅ BE-000 Setup & Skeleton — merged (PR #21) — main@HEAD: abad338027ebc2a13688b85bd6e72bad60afdf04
- ✅ BE-010 Auth Middleware — verified by gap review; no new implementation PR required
- ✅ BE-020 Create Inspection Session — merged (PR #23) — main@HEAD: f85c7b669c0e814cc655fbb10c3bd1ce5466a9b7
- ✅ BE-030 Complete Upload & Queueing — merged (PR #26) — main@HEAD: b663fccccc68d910cc7e92cc5d354361e6872260
- ✅ BE-040 Inspection Status — merged (PR #28) — main@HEAD: 388e614b922f493846f28183c30ec450d30a3f28
  - Follow-up: internal `queued` status is currently mapped to public `pending`; revisit lifecycle mapping during BE-060.

## 2026-06-05

* ✅ BE-050 Inspection Result — merged (PR #32) — main@HEAD: 5bbd5883a52cb2afadab789362c8ceb4b7b897ef
  * Follow-up: BE-060 must connect queued jobs to processing/completed/failed lifecycle and populate persisted results from the inference stub worker.
  * Follow-up: lifecycle integrity must be enforced: an inspection should not become `completed` before its result is persisted.
  * Follow-up: current `queued` to public `pending` mapping remains unchanged and should be revisited during BE-060.

* ✅ BE-060 Inference Stub Worker — merged (PR #34) — main@HEAD: 620ea5a63d6136c34bd14e983f30c87f7da60e4e
  * Completed: added inference stub worker with deterministic mocked outputs per mode.
  * Completed: added queue consumption via `InMemoryJobQueue.pop_by_inspection_id()`.
  * Completed: added `run_next_job(...)` safe worker entrypoint.
  * Completed: result is persisted before inspection becomes `completed`.
  * Completed: retry-safety/idempotency prevents overwriting existing completed results or changing `created_at`.
  * Follow-up: real AI inference remains out of scope for MVP backend stubs.
  * Follow-up: Celery/Redis production worker wiring remains future work.
  * Follow-up: public status mapping still exposes internal `queued` as `pending`; revisit public `processing` visibility in a future lifecycle/API ticket.
  * Follow-up: in-memory stores are not persistent and must later move to real database-backed storage.




