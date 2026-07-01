import os
import sys
import pytest

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(BACKEND)

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_ioc_summary():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/reports/ioc-summary")
    assert response.status_code == 200
    data = response.json()
    assert "ioc_count" in data
