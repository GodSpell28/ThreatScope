from fastapi import APIRouter, Query
from app.services.search import ensure_index, index_ioc, search_iocs

router = APIRouter()


@router.post("/setup")
async def setup_index():
    return ensure_index()


@router.post("/index")
async def index_document(doc: dict[str, Any]):
    return index_ioc(doc)


@router.get("/query")
async def query_index(q: str = Query(..., min_length=1), size: int = 50):
    return search_iocs(q, size=size)
