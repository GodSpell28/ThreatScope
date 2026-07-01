from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class IOCSourceCreate(BaseModel):
    source_name: str
    external_id: Optional[str] = None
    raw: Optional[str] = None


class IOCCreate(BaseModel):
    type: str
    value: str
    confidence: float = 0.0
    sources: List[IOCSourceCreate] = []


class IOCSourceResponse(IOCSourceCreate):
    id: int
    fetched_at: datetime

    class Config:
        from_attributes = True


class IOCResponse(BaseModel):
    id: str
    type: str
    value: str
    risk_score: float
    confidence: float
    first_seen: datetime
    last_seen: datetime
    sources: List[IOCSourceResponse] = []

    class Config:
        from_attributes = True


class IngestResponse(BaseModel):
    ingested: int
    duplicates: int
    iocs: List[IOCResponse]
