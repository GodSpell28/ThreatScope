from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.ioc import IOC
from app.services.correlation import correlate_iocs

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/run")
async def run_correlation(db: Session = Depends(get_db)):
    iocs = db.query(IOC).all()
    results = correlate_iocs(iocs)
    return {
        "ioc_count": len(iocs),
        "correlations": [
            {"source_id": a, "related_id": b, "score": score}
            for a, b, score in results
        ],
    }
