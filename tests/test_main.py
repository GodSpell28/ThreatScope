import os
import sys
import pytest

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(BACKEND)

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_ingest_raw():
    transport = ASGITransport(app=app)
    payload = [
        {"type": "ipv4", "value": "198.51.100.10", "confidence": 0.8, "sources": [{"source_name": "abuseipdb"}]},
        {"type": "domain", "value": "malicious.example", "confidence": 0.9, "sources": [{"source_name": "vt"}]},
    ]
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/ingest/raw", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["ingested"] == 2
