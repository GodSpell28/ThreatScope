import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        reg = await client.post("/api/v1/auth/register", json={
            "username": "interviewer",
            "email": "interview@example.com",
            "password": "secret123",
            "role": "analyst",
        })
    assert reg.status_code == 200
    assert reg.json()["role"] == "analyst"

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        login = await client.post("/api/v1/auth/login", json={
            "username": "interviewer",
            "password": "secret123",
        })
    assert login.status_code == 200
    token = login.json()["access_token"]
    assert token.startswith("token-")
    assert login.json()["role"] == "analyst"


@pytest.mark.asyncio
async def test_me_endpoint_and_scopes():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/v1/auth/register", json={
            "username": "admin1",
            "email": "admin1@example.com",
            "password": "secret123",
            "role": "admin",
        })

        login = await client.post("/api/v1/auth/login", json={
            "username": "admin1",
            "password": "secret123",
        })
    token = login.json()["access_token"]

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/auth/me", headers={"x-token": token})
    assert r.status_code == 200
    data = r.json()
    assert data["role"] == "admin"
    assert isinstance(data["scopes"], list)
    assert "users:write" in data["scopes"]


@pytest.mark.asyncio
async def test_ioc_search_forbidden_to_unknown_role_when_no_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/iocs/search")
    assert r.status_code == 422
