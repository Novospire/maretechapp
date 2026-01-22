# Tech Stack — Maretech Mobile App
Version: v1.0  
Status: Locked for MVP (Python-heavy)

---

## 1) Goals
- Build a working, testable mobile MVP fast
- Async-first AI processing
- Minimal moving parts
- Clear separation: API vs worker

---

## 2) Chosen Stack (MVP)

### Mobile
- React Native (Expo)

### Backend API
- Python FastAPI
- JWT auth (backend validates bearer token)

### Async Jobs
- Celery workers for AI jobs
- Redis as Celery broker (and optional cache)

### Database
- PostgreSQL
- Stores inspections, results, subscriptions/payment flags, model_version

### Object Storage
- S3-compatible storage (AWS S3 or MinIO)
- Presigned URLs for image upload/download

---

## 3) Why Not Hybrid (Supabase/Auth/Edge)
- Adds system boundaries and duplicated logic
- Increases integration and debugging overhead
- Not required for MVP validation

---

## 4) Deployment (MVP)
- API service: FastAPI
- Worker service: Celery
- Redis: managed or container
- Postgres: managed or container
- S3: managed or MinIO

---

## 5) Non-Negotiables (from Context Pack)
- No diagnosis, non-binding language
- Osmosis and Corrosion are separate products under one app shell
- Async inference only (no blocking inference in API)
