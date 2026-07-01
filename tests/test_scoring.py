import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_score_returns_recommendation():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ingest = await client.post("/api/v1/ingest/raw", json={
            "iocs": [{"type": "ipv4", "value": "10.0.0.2", "risk_score": 10, "confidence": 0.1}],
            "sources": [{"source_name": "unit-test"}],
        })
    assert ingest.status_code == 200
    ioc_id = ingest.json()["iocs"][0]["id"]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(f"/api/v1/score/{ioc_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == ioc_id
    assert body["risk_score"] >= 0
    assert "recommendation" in body


@pytest.mark.asyncio
async def test_batch_score_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/ingest/raw", json={
            "iocs": [
                {"type": "ipv4", "value": "10.0.0.3", "risk_score": 10, "confidence": 0.1},
                {"type": "domain", "value": "ok.example", "risk_score": 40, "confidence": 0.4},
            ],
            "sources": [{"source_name": "unit-test"}],
        })

        r = await client.get("/api/v1/score/")
    assert r.status_code == 200
    assert len(r.json()) >= 2
