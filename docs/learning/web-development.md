# Web Development

Notes on frontend/web concepts: Server Components, Client Components, SSR, streaming, OAuth, Next.js App Router patterns.

---

### How to test a FastAPI endpoint locally
**Date:** 2026-06-09
**Context:** Testing the POST /ingest endpoint end-to-end
**Answer/Decision:** 1) Start the server: `uv run uvicorn chronicle.api:app --reload --port 8001` (--reload = hot-reload on code changes). 2) Test with curl: `curl -X POST http://localhost:8001/ingest -H "Content-Type: application/json" -d '{...}'`. 3) Or use FastAPI's built-in Swagger UI at `http://localhost:8001/docs` — interactive browser-based testing without curl. Verify results in Supabase dashboard Table Editor.

---

