import os
import sys

BACKEND = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.append(BACKEND)

from httpx import AsyncClient, ASGITransport
from app.main import app


def test_health_without_auth():
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    # ensure app starts without auth
    response = client.get("/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
