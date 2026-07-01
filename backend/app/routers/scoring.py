from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.ioc import IOC
from app.services.scoring import calculate_ioc_risk, calculate_batch_risk

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{ioc_id}")
async def get_ioc_score(ioc_id: str, db: Session = Depends(get_db)):
    ioc = db.get(IOC, ioc_id)
    if not ioc:
        return {"error": "IOC not found", "id": ioc_id}
    return {"id": ioc.id, "type": ioc.type, "value": ioc.value, **calculate_ioc_risk(ioc)}


@router.get("/")
async def list_scores(db: Session = Depends(get_db)):
    iocs = db.query(IOC).limit(100).all()
    return calculate_batch_risk(iocs)
