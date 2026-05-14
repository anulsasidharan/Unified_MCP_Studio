"""Auth API integration tests (require PostgreSQL)."""

import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_login_me(async_client_db: AsyncClient):
    email = f"user-{uuid.uuid4().hex[:8]}@example.com"
    r = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123", "name": "Test User"},
    )
    assert r.status_code == 201, r.text
    token = r.json()["access_token"]
    assert token

    me = await async_client_db.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == 200
    body = me.json()
    assert body["email"] == email
    assert body["name"] == "Test User"
    assert body["tier"] == "free"

    login = await async_client_db.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client_db: AsyncClient):
    email = f"dup-{uuid.uuid4().hex[:8]}@example.com"
    body = {"email": email, "password": "password123"}
    r1 = await async_client_db.post("/api/v1/auth/register", json=body)
    assert r1.status_code == 201
    r2 = await async_client_db.post("/api/v1/auth/register", json=body)
    assert r2.status_code == 409
    err = r2.json()["error"]
    assert err["code"] == "EMAIL_TAKEN"


@pytest.mark.asyncio
async def test_me_without_token(async_client_db: AsyncClient):
    r = await async_client_db.get("/api/v1/auth/me")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_logout(async_client_db: AsyncClient):
    email = f"out-{uuid.uuid4().hex[:8]}@example.com"
    reg = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"},
    )
    token = reg.json()["access_token"]
    out = await async_client_db.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert out.status_code == 204
