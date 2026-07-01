import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_empty_search():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/iocs/search", params={"limit": 1, "min_risk": 999})
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.asyncio
async def test_ingest_then_search():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ingest = await client.post("/api/v1/ingest/raw", json={
            "iocs": [{"type": "ipv4", "value": "10.0.0.1", "risk_score": 55, "confidence": 0.5}],
            "sources": [{"source_name": "unit-test"}]
        })
    assert ingest.status_code == 200

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/iocs/search", params={"q": "10.0.0.1"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["value"] == "10.0.0.1"
