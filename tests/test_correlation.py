import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_correlation_run():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/ingest/raw", json={
            "iocs": [
                {"type": "ipv4", "value": "10.0.0.1", "risk_score": 40, "confidence": 0.5},
                {"type": "ipv4", "value": "10.0.0.1", "risk_score": 60, "confidence": 0.7},
            ],
            "sources": [{"source_name": "unit-test"}]
        })

        r = await client.get("/api/v1/correlation/run")
    assert r.status_code == 200
    assert r.json()["ioc_count"] == 1
