import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_score_endpoint_shape():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ingest = await client.post("/api/v1/ingest/raw", json={
            "iocs": [{"type": "ipv4", "value": "10.0.0.2", "risk_score": 10, "confidence": 0.1}],
            "sources": [{"source_name": "unit-test"}]
        })
    assert ingest.status_code == 200
    ioc_id = ingest.json()["iocs"][0]["id"]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get(f"/api/v1/score/{ioc_id}")
    assert r.status_code == 200
    body = r.json()
    for key in ["id", "risk_score", "confidence", "source_count", "recommendation"]:
        assert key in body
