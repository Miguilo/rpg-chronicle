from pydantic import BaseModel
from uuid import UUID

class IngestRequest(BaseModel):
    transcription: str
    session_id: UUID
    session_title: str | None = None


class IngestResponse(BaseModel):
    chunk_count: int
    success: str