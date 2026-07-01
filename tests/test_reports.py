import pytest

from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_ioc_summary_shape():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/reports/ioc-summary")
    assert r.status_code == 200
    body = r.json()
    for key in ["ioc_count", "high_risk_count", "medium_risk_count", "low_risk_count", "avg_risk_score", "type_distribution", "source_frequency"]:
        assert key in body
