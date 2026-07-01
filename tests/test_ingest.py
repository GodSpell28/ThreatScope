import os
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "threatscope"


@pytest.mark.asyncio
async def test_ingest_raw_creates_ioc():
    transport = ASGITransport(app=app)
    payload = {
        "iocs": [
            {"type": "ipv4", "value": "10.0.0.10", "risk_score": 70, "confidence": 0.8},
            {"type": "domain", "value": "evil.example", "risk_score": 88, "confidence": 0.9},
        ],
        "sources": [
            {"source_name": "unit-test-1"},
            {"source_name": "unit-test-2", "external_id": "ex-1"},
        ],
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/ingest/raw", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["ingested"] == 2
    assert body["duplicates"] == 0
    assert len(body["iocs"]) == 2
    assert body["iocs"][0]["id"].startswith("sha256-")


@pytest.mark.asyncio
async def test_ingest_raw_dedup_and_recommendation():
    transport = ASGITransport(app=app)
    payload = {
        "iocs": [
            {"type": "ipv4", "value": "10.0.0.10", "risk_score": 70, "confidence": 0.8},
        ],
        "sources": [{"source_name": "unit-test-dup"}],
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.post("/api/v1/ingest/raw", json=payload)
    assert first.status_code == 200
    assert first.json()["ingested"] == 1

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        second = await client.post("/api/v1/ingest/raw", json=payload)
    assert second.status_code == 200
    assert second.json()["duplicates"] == 1
    assert second.json()["iocs"][0]["value"] == "10.0.0.10"
    assert second.json()["iocs"][0]["risk_score"] >= 70
