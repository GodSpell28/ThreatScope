import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_ioc_summary_shape():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/ingest/raw", json={
            "iocs": [
                {"type": "ipv4", "value": "10.0.0.20", "risk_score": 90, "confidence": 0.9},
                {"type": "domain", "value": "ok.example", "risk_score": 20, "confidence": 0.3},
            ],
            "sources": [{"source_name": "unit-test"}],
        })

        r = await client.get("/api/v1/reports/ioc-summary")
    assert r.status_code == 200
    body = r.json()
    assert body["ioc_count"] == 2
    assert body["high_risk_count"] >= 1
    assert body["low_risk_count"] >= 1
    for key in ["avg_risk_score", "type_distribution", "source_frequency"]:
        assert key in body


@pytest.mark.asyncio
async def test_threat_summary_shape():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/reports/threat-summary")
    assert r.status_code == 200
    body = r.json()
    assert "technique_coverage_count" in body
    assert isinstance(body["top_techniques"], list)
