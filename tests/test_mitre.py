import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_mitre_search_and_mapping():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/mitre/search", params={"q": "phish"})
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, list)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        ingest = await client.post("/api/v1/ingest/raw", json={
            "iocs": [{"type": "domain", "value": "phish.example", "risk_score": 55, "confidence": 0.6}],
            "sources": [{"source_name": "unit-test"}],
        })
    assert ingest.status_code == 200
    ioc_id = ingest.json()["iocs"][0]["id"]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/mitre/search", params={"q": "phish", "limit": 1})
    assert r.status_code == 200
    techniques = r.json()
    assert len(techniques) >= 1

    technique_id = techniques[0]["id"]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        map_r = await client.post(f"/api/v1/mitre/{ioc_id}/map/{technique_id}")
    assert map_r.status_code == 200

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        list_r = await client.get(f"/api/v1/mitre/{ioc_id}")
    assert list_r.status_code == 200
    body = list_r.json()
    assert isinstance(body, list)
