# Python Patterns

Notes on Python-specific patterns, idioms, and common mistakes learned during development.

---

### Attribute access vs subscript access on SDK response objects
**Date:** 2026-06-09
**Context:** Implementing embedder.py — extracting vectors from OpenAI API response
**Answer/Decision:** SDK responses (like OpenAI's) return Pydantic objects, not dicts or lists. You access their fields with dot notation (`response.data[0].embedding`), not brackets (`response[1][0][0]`). Brackets (`[]`) are for lists/dicts; dots (`.`) are for object attributes. `TypeError: object is not subscriptable` means you're using brackets on something that isn't a list or dict.

---

### `__init__.py` vs package manager (uv) — different layers
**Date:** 2026-06-09
**Context:** Importing `chronicle.services.chunker` in api.py
**Answer/Decision:** `uv` (or pip) resolves where the package lives on disk. `__init__.py` controls what's accessible when you import the package namespace. An empty `__init__.py` means sub-modules aren't auto-loaded — `import chronicle.services as services; services.chunker` fails with AttributeError. Fix: either populate `__init__.py` with explicit imports, or import directly: `from chronicle.services.chunker import chunk_text`. Direct imports are more explicit and the modern Python convention.

---

### Don't silently swallow errors with bare except in development
**Date:** 2026-06-09
**Context:** POST /ingest endpoint error handling in api.py
**Answer/Decision:** Wrapping code in `try: ... except: return error_response` hides bugs — you don't know WHY it failed. In Phase 0 (local dev), let errors explode: FastAPI returns a 500 with the traceback, which tells you exactly what broke. Only add error handling when you have a clear recovery strategy. If you must catch, use `except Exception as e:` and at minimum `print(e)` so you can debug.

---

### SSL CERTIFICATE_VERIFY_FAILED on macOS with uv-managed Python
**Date:** 2026-06-09
**Context:** Supabase client failing to connect via HTTPS when running the /ingest endpoint
**Answer/Decision:** Python installed via `uv` (standalone) doesn't automatically find macOS system certificates. Fix: use `truststore` library — call `truststore.inject_into_ssl()` at the top of the app entry point (before any HTTP imports). This tells Python to use the OS certificate store. Already had `certifi` and `truststore` in dependencies, just needed to activate it.

---

