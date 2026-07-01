import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_es_setup():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/search/setup")
    assert r.status_code == 200
    data = r.json()
    assert data["index"] == "threatscope-iocs"


@pytest.mark.asyncio
async def test_es_index_and_search():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        setup = await client.post("/api/v1/search/setup")
        assert setup.status_code == 200

        index = await client.post("/api/v1/search/index", json={"id": "s1", "type": "ipv4", "value": "1.2.3.4", "risk_score": 75, "confidence": 0.8, "source_count": 1})
        assert index.status_code == 200

        query = await client.get("/api/v1/search/query", params={"q": "1.2.3.4", "size": 5})
    assert query.status_code == 200
    data = query.json()
    assert data["count"] >= 1
