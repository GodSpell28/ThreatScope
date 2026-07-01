import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_sigma_rule_lifecycle():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Demo Sigma Rule",
        "rule_type": "sigma",
        "content": "title: Demo\ndetection:\n  selection:\n    Image|endswith: powershell.exe\n  condition: selection",
        "status": "draft",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/rules/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == payload["name"]

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        validate = await client.post(f"/api/v1/rules/{data['id']}/validate")
    assert validate.status_code == 200
    assert validate.json()["valid"] is True


@pytest.mark.asyncio
async def test_yara_rule_lifecycle():
    transport = ASGITransport(app=app)
    payload = {
        "name": "Demo YARA Rule",
        "rule_type": "yara",
        "content": "rule Demo { condition: true }",
        "status": "draft",
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/api/v1/rules/", json=payload)
    assert r.status_code == 200
    assert r.json()["rule_type"] == "yara"
