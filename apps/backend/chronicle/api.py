"""
MVP API for the RPG Chronicle pipeline.

Phase 0: single endpoint that receives raw text, chunks it,
generates embeddings, and saves to Supabase.

This is intentionally simple — no queue, no auth, no audio processing.
Just text in → chunks + embeddings out.
"""
from fastapi import FastAPI
from chronicle.models import IngestRequest, IngestResponse
from chronicle.clients.supabase_client import get_supabase_client
from chronicle.services.chunker import chunk_text
from chronicle.services.embedder import generate_embeddings
import truststore
truststore.inject_into_ssl()

app = FastAPI(title="RPG Chronicle Pipeline")

@app.post("/ingest", response_model = IngestResponse)
def ingest(request: IngestRequest):
    """Ingest transcription: chunk, embed, and store in Supabase"""
    transcription = request.transcription
    chunks = chunk_text(transcription, chunk_size=10, overlap=5)
    contents = [chunk["content"] for chunk in chunks]
    embeddings = generate_embeddings(contents)
    supabase_client = get_supabase_client()
    rows = []

    # adding rows regard to chunks
    for idx, embedding in enumerate(embeddings):
        content = contents[idx]
        chunk_idx = chunks[idx]["chunk_index"]

        row = {
            "content": content,
            "chunk_index": chunk_idx,
            "embedding": embedding,
            "session_id": str(request.session_id),
            "campaign_id": str(request.campaign_id),
        }

        rows.append(row)

    supabase_client.table("session_chunks").insert(rows).execute()


    return IngestResponse(chunk_count=len(embeddings), success=True)


@app.get("/health")
async def health():
    return {"status": "ok"}
