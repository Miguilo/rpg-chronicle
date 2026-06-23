from pydantic import BaseModel
from uuid import UUID

class IngestRequest(BaseModel):
    transcription: str
    session_id: UUID
    session_title: str | None = None
    campaign_id: UUID


class IngestResponse(BaseModel):
    chunk_count: int
    success: bool