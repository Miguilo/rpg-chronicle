"""
MVP API for the RPG Chronicle pipeline.

Phase 0: single endpoint that receives raw text, chunks it,
generates embeddings, and saves to Supabase.

This is intentionally simple — no queue, no auth, no audio processing.
Just text in → chunks + embeddings out.
"""

from fastapi import FastAPI

app = FastAPI(title="RPG Chronicle Pipeline")


@app.get("/health")
async def health():
    return {"status": "ok"}
