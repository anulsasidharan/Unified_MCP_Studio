"""Auth API integration tests (require PostgreSQL)."""

import os
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.session import get_db
from app.main import app
from app.models.base import Base

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://mcpstudio:mcpstudio@127.0.0.1:5432/mcpstudio",
    ),
)


@pytest.fixture
async def async_client_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except OSError as exc:
        await engine.dispose()
        pytest.skip(f"PostgreSQL not reachable: {exc}")
    except Exception as exc:
        await engine.dispose()
        pytest.skip(f"PostgreSQL not available: {exc}")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_db():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


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
