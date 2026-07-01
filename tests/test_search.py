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

        index = await client.post("/api/v1/search/index", json={
            "id": "s-search-1",
            "type": "domain",
            "value": "demo.example",
            "risk_score": 81,
            "confidence": 0.85,
            "source_count": 2,
            "first_seen": "2026-06-01T00:00:00Z",
            "last_seen": "2026-06-25T00:00:00Z",
        })
        assert index.status_code == 200

        query = await client.get("/api/v1/search/query", params={"q": "demo.example", "size": 5})
    assert query.status_code == 200
    data = query.json()
    assert data["count"] >= 1
    assert data["results"][0]["id"] == "s-search-1"


@pytest.mark.asyncio
async def test_es_query_without_setup_succeeds():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/search/query", params={"q": "nothing-here", "size": 1})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 0
