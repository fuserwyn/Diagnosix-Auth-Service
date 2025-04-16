# tests/test_api.py
import pytest
from httpx import AsyncClient

API_BASE = "http://localhost:8000"

@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(base_url=API_BASE) as client:
        response = await client.post(f"{API_BASE}/register", json={
            "email": "user1@example.com",
            "password": "123456",
            "role": "doctor"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user1@example.com"
        assert data["role"] == "doctor"


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(base_url=API_BASE) as client:
        await client.post(f"{API_BASE}/register", json={
            "email": "user2@example.com",
            "password": "123456",
            "role": "patient"
        })
        response = await client.post(f"{API_BASE}/login", json={
            "email": "user2@example.com",
            "password": "123456"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_me():
    async with AsyncClient(base_url=API_BASE) as client:
        await client.post(f"{API_BASE}/register", json={
            "email": "user3@example.com",
            "password": "123456",
            "role": "admin"
        })
        login = await client.post(f"{API_BASE}/login", json={
            "email": "user3@example.com",
            "password": "123456"
        })
        token = login.json()["access_token"]

        response = await client.get(f"{API_BASE}/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "user3@example.com"
        assert data["role"] == "admin"