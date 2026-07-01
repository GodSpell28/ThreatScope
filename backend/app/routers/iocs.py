from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import SessionLocal
from app.models.ioc import IOC
from app.schemas.ioc import IOCResponse
from app.services.auth import scopes_for_role, fake_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/search", response_model=List[IOCResponse])
async def search_iocs(
    q: Optional[str] = None,
    type: Optional[str] = None,
    min_risk: float = 0.0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: "User" = Depends(fake_current_user),
):
    if "iocs:read" not in scopes_for_role(current_user.role):
        raise HTTPException(status_code=403, detail="Forbidden")
    query = db.query(IOC)
    if type:
        query = query.filter(IOC.type == type)
    if q:
        query = query.filter(IOC.value.ilike(f"%{q}%"))
    query = query.filter(IOC.risk_score >= min_risk).order_by(IOC.risk_score.desc()).limit(limit)
    iocs = query.all()
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
        for i in iocs
    ]


@router.get("/{ioc_id}", response_model=IOCResponse)
async def get_ioc(ioc_id: str, db: Session = Depends(get_db), current_user: "User" = Depends(fake_current_user)):
    if "iocs:read" not in scopes_for_role(current_user.role):
        raise HTTPException(status_code=403, detail="Forbidden")
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
        sources=[],
    )
