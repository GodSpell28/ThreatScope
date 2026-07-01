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
            "sources": [{"source_name": "unit-test"}],
        })
    assert ingest.status_code == 200

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/iocs/search", params={"q": "10.0.0.1"})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["value"] == "10.0.0.1"


@pytest.mark.asyncio
async def test_search_by_type_and_min_risk():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/ingest/raw", json={
            "iocs": [
                {"type": "ipv4", "value": "10.0.0.2", "risk_score": 20, "confidence": 0.2},
                {"type": "domain", "value": "ok.example", "risk_score": 85, "confidence": 0.9},
            ],
            "sources": [{"source_name": "unit-test"}],
        })

        r = await client.get("/api/v1/iocs/search", params={"type": "domain", "min_risk": 70})
    assert r.status_code == 200
    body = r.json()
    assert len(body) == 1
    assert body[0]["type"] == "domain"
    assert body[0]["value"] == "ok.example"
