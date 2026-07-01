from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ioc import IOC, IOCSource

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{ioc_id}/enrich")
async def enrich_ioc(ioc_id: str, db: Session = Depends(get_db)):
    ioc = db.get(IOC, ioc_id)
    if not ioc:
        raise HTTPException(status_code=404, detail="IOC not found")

    # Demo enrichment: append a demo source entry
    db.add(IOCSource(ioc_id=ioc.id, source_name="demo_enrichment", raw='{"demo": true}'))
    db.commit()
    return {"id": ioc.id, "enriched": True, "sources": [s.source_name for s in ioc.sources]}
