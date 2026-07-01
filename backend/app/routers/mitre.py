from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.technique import Technique

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search")
async def search_techniques(q: str = "", tactic: str = "", db: Session = Depends(get_db)):
    query = db.query(Technique)
    if q:
        query = query.filter(Technique.name.ilike(f"%{q}%"))
    if tactic:
        query = query.filter(Technique.tactic == tactic)
    techniques = query.limit(100).all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "tactic": t.tactic,
            "description": t.description,
        }
        for t in techniques
    ]


@router.post("/{ioc_id}/map/{technique_id}")
async def map_ioc_to_technique(ioc_id: str, technique_id: str, db: Session = Depends(get_db)):
    from app.models.ioc import IOC, ioc_technique
    from sqlalchemy import insert

    ioc = db.get(IOC, ioc_id)
    technique = db.get(Technique, technique_id)
    if not ioc or not technique:
        raise HTTPException(status_code=404, detail="IOC or technique not found")

    exists = db.query(ioc_technique).filter_by(ioc_id=ioc_id, technique_id=technique_id).first()
    if not exists:
        stmt = insert(ioc_technique).values(ioc_id=ioc_id, technique_id=technique_id)
        db.execute(stmt)
        db.commit()
    return {"mapped": True, "ioc_id": ioc_id, "technique_id": technique_id}


@router.get("/{ioc_id}")
async def get_ioc_techniques(ioc_id: str, db: Session = Depends(get_db)):
    from app.models.ioc import IOC
    ioc = db.get(IOC, ioc_id)
    if not ioc:
        raise HTTPException(status_code=404, detail="IOC not found")
    return [
        {"id": t.id, "name": t.name, "tactic": t.tactic}
        for t in ioc.techniques
    ]
