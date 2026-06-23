# Concepts

Notes on domain concepts: chunking, embeddings, RAG, vector search, RLS, queues, and other backend/ML fundamentals.

---

### API Batching — sending multiple inputs in one call
**Date:** 2026-06-09
**Context:** Implementing embedder.py (generate_embeddings function)
**Answer/Decision:** The OpenAI embeddings API accepts a list of strings in a single `input` parameter. Sending all texts at once (batch) is far more efficient than looping and making one HTTP call per text. 50 chunks = 1 request instead of 50. Also important: the API response object contains metadata — you need to extract `.data[i].embedding` to get the actual float vectors.

---

### Wiring an endpoint — connecting pipeline steps
**Date:** 2026-06-09
**Context:** Building the POST /ingest endpoint in api.py
**Answer/Decision:** The `/ingest` endpoint is the "DAG" of the pipeline: receives text → chunks it → generates embeddings → saves to DB. In Phase 0 it's synchronous and simple (no queue). FastAPI has `Depends()` for dependency injection, but it's overkill in Phase 0 — just call functions directly. Use `Depends()` in Phase 1+ for auth, DB sessions, etc.

---

### Supabase .insert() expects list of dicts, not list of lists
**Date:** 2026-06-09
**Context:** Building the POST /ingest endpoint — inserting chunks into session_chunks table
**Answer/Decision:** `supabase_client.table("x").insert(rows).execute()` expects `rows` to be a list of dictionaries where keys match column names: `[{"content": "...", "chunk_index": 0, "embedding": [...], "session_id": "..."}]`. Not a list of lists/tuples. Also, UUID fields must be converted to strings with `str()` before inserting.

---

