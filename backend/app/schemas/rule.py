from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.rule import RuleType


class RuleCreate(BaseModel):
    name: str
    rule_type: RuleType
    content: str
    status: Optional[str] = "draft"


class RuleResponse(BaseModel):
    id: int
    name: str
    rule_type: RuleType
    content: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
