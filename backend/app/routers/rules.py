from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.rule import DetectionRule, RuleType
from app.schemas.rule import RuleCreate, RuleResponse
from app.services.rules import summarize_rule, validate_rule

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=RuleResponse)
async def create_rule(rule: RuleCreate, db: Session = Depends(get_db)):
    db_rule = DetectionRule(**rule.model_dump())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule


@router.get("/", response_model=List[RuleResponse])
async def list_rules(rule_type: RuleType | None = None, db: Session = Depends(get_db)):
    query = db.query(DetectionRule)
    if rule_type:
        query = query.filter(DetectionRule.rule_type == rule_type)
    return query.limit(200).all()


@router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.get(DetectionRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.post("/{rule_id}/validate")
async def validate_rule_endpoint(rule_id: int, db: Session = Depends(get_db)):
    rule = db.get(DetectionRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return validate_rule(rule)


@router.get("/{rule_id}/summary")
async def rule_summary(rule_id: int, db: Session = Depends(get_db)):
    rule = db.get(DetectionRule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return summarize_rule(rule)
