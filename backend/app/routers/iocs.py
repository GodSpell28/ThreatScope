from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import SessionLocal
from app.models.ioc import IOC, IOCSource
from app.schemas.ioc import IOCResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search", response_model=list[IOCResponse])
async def search_iocs(
    q: Optional[str] = None,
    type: Optional[str] = None,
    min_risk: float = 0.0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    query = db.query(IOC)
    if type:
        query = query.filter(IOC.type == type)
    if q:
        query = query.filter(IOC.value.ilike(f"%{q}%"))
    query = query.filter(IOC.risk_score >= min_risk).order_by(IOC.risk_score.desc()).limit(limit)
    results = query.all()
    return [
        IOCResponse(
            id=i.id,
            type=i.type,
            value=i.value,
            risk_score=i.risk_score,
            confidence=i.confidence,
            first_seen=i.first_seen,
            last_seen=i.last_seen,
            sources=[],
        )
        for i in results
    ]


@router.get("/{ioc_id}", response_model=IOCResponse)
async def get_ioc(ioc_id: str, db: Session = Depends(get_db)):
    ioc = db.get(IOC, ioc_id)
    if not ioc:
        raise HTTPException(status_code=404, detail="IOC not found")
    return IOCResponse(
        id=ioc.id,
        type=ioc.type,
        value=ioc.value,
        risk_score=ioc.risk_score,
        confidence=ioc.confidence,
        first_seen=ioc.first_seen,
        last_seen=ioc.last_seen,
        sources=[
            IOCResponse.Source(
                id=s.id,
                source_name=s.source_name,
                external_id=s.external_id,
                fetched_at=s.fetched_at,
            )
            for s in ioc.sources
        ],
    )
