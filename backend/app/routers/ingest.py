from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.schemas.ioc import IOCCreate, IngestResponse
from app.models.base import SessionLocal
from app.services.ingestion import ingest_raw_iocs, ingest_stix_bundle

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/raw", response_model=IngestResponse)
async def ingest_raw(items: List[IOCCreate], db: Session = Depends(get_db)):
    payload = [i.model_dump() for i in items]
    result = ingest_raw_iocs(db, payload)
    return IngestResponse(**result, iocs=result.get("iocs", []))


@router.post("/stix", response_model=IngestResponse)
async def ingest_stix(bundle: Dict[str, Any], db: Session = Depends(get_db)):
    if bundle.get("type") != "bundle":
        raise HTTPException(status_code=400, detail="Expected a STIX bundle")
    result = ingest_stix_bundle(db, bundle)
    return IngestResponse(**result, iocs=result.get("iocs", []))
