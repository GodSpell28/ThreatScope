import os
import sys
import pytest

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(BACKEND)

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_sigma_rule():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Demo Sigma Rule",
        "rule_type": "sigma",
        "content": "title: Demo\ndetection:\n  selection:\n    Image|endswith: powershell.exe\n  condition: selection",
        "status": "draft",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/rules/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Demo Sigma Rule"
    assert data["rule_type"] == "sigma"


@pytest.mark.asyncio
async def test_create_yara_rule():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Demo YARA Rule",
        "rule_type": "yara",
        "content": "rule Demo { condition: true }",
        "status": "draft",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/rules/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["rule_type"] == "yara"
