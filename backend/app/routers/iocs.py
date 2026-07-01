from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class IOCRequest(BaseModel):
    indicator: str
    type: str


class IOCResponse(BaseModel):
    id: str
    indicator: str
    type: str
    risk_score: float
    sources: list[str]
    mitre_techniques: list[str]


@router.post("/search", response_model=IOCResponse)
async def search_ioc(request: IOCRequest):
    return IOCResponse(
        id="demo-1",
        indicator=request.indicator,
        type=request.type,
        risk_score=0.0,
        sources=[],
        mitre_techniques=[],
    )
