import pytest

from httpx import AsyncClient
from fastapi import status


API_BASE = "http://localhost:8000"


@pytest.mark.asyncio
async def test_register():
    async with AsyncClient(base_url=API_BASE) as client:
        response = await client.post(f"{API_BASE}/register", json={
            "email": "user1@example.com",
            "password": "123456ppp",
            "role": "doctor"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "user1@example.com"
        assert data["role"] == "doctor"


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(base_url=API_BASE) as client:
        await client.post(f"{API_BASE}/register", json={
            "email": "user2@example.com",
            "password": "123456ppp",
            "role": "patient"
        })
        response = await client.post(f"{API_BASE}/login", json={
            "email": "user2@example.com",
            "password": "123456ppp"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_me():
    async with AsyncClient(base_url=API_BASE) as client:
        await client.post(f"{API_BASE}/register", json={
            "email": "user3@example.com",
            "password": "123456ppp",
            "role": "admin"
        })
        login = await client.post(f"{API_BASE}/login", json={
            "email": "user3@example.com",
            "password": "123456ppp"
        })
        token = login.json()["access_token"]

        response = await client.get(f"{API_BASE}/me", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == "user3@example.com"
        assert data["role"] == "admin"


@pytest.mark.asyncio
async def test_admin_access_granted():
    async with AsyncClient(base_url=API_BASE) as client:
        await client.post("/register", json={
            "email": "admin1@example.com",
            "password": "adminpass111",
            "role": "admin"
        })
        login = await client.post("/login", json={
            "email": "admin1@example.com",
            "password": "adminpass111"
        })
        token = login.json()["access_token"]

        response = await client.get("/dashboard", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == status.HTTP_200_OK
        assert "Welcome, admin" in response.json()["message"]


@pytest.mark.asyncio
async def test_doctor_access_denied(clear_users_after_test):
    async with AsyncClient(base_url=API_BASE) as client:
        await client.post("/register", json={
            "email": "doc@example.com",
            "password": "docpass111",
            "role": "doctor"
        })
        login = await client.post("/login", json={
            "email": "doc@example.com",
            "password": "docpass111"
        })
        token = login.json()["access_token"]

        response = await client.get("/dashboard", headers={
            "Authorization": f"Bearer {token}"
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN
