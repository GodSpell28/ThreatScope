from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.ioc import IOC
from app.models.technique import Technique
from app.services.reporting import generate_ioc_report, generate_threat_report

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/ioc-summary")
async def ioc_summary(limit: int = 200, db: Session = Depends(get_db)):
    iocs = db.query(IOC).limit(limit).all()
    return generate_ioc_report(iocs)


@router.get("/threat-summary")
async def threat_summary(limit: int = 200, db: Session = Depends(get_db)):
    iocs = db.query(IOC).limit(limit).all()
    techniques = db.query(Technique).all()
    return generate_threat_report(iocs, techniques)
