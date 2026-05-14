"""POST /api/v1/projects/from-catalog-blueprint and /from-blueprint-export."""

import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_from_catalog_blueprint_requires_auth(async_client_db: AsyncClient):
    r = await async_client_db.post(
        "/api/v1/projects/from-catalog-blueprint",
        json={"blueprint_id": "basic-echo-json"},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_from_catalog_blueprint_unknown(async_client_db: AsyncClient):
    email = f"cat-{uuid.uuid4().hex[:8]}@example.com"
    reg = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"},
    )
    token = reg.json()["access_token"]
    r = await async_client_db.post(
        "/api/v1/projects/from-catalog-blueprint",
        headers={"Authorization": f"Bearer {token}"},
        json={"blueprint_id": "does-not-exist-xyz"},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_from_catalog_blueprint_creates_project_and_tools(async_client_db: AsyncClient):
    email = f"cat-{uuid.uuid4().hex[:8]}@example.com"
    reg = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"},
    )
    token = reg.json()["access_token"]

    r = await async_client_db.post(
        "/api/v1/projects/from-catalog-blueprint",
        headers={"Authorization": f"Bearer {token}"},
        json={"blueprint_id": "basic-echo-json", "name": "Echo project"},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["name"] == "Echo project"
    assert body["runtime"] == "typescript"
    assert body["transport"] == "stdio"
    pid = body["id"]

    tools = await async_client_db.get(
        f"/api/v1/projects/{pid}/tools",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert tools.status_code == 200
    listed = tools.json()
    assert len(listed) == 2
    names = {row["name"] for row in listed}
    assert names == {"echo", "ping"}


@pytest.mark.asyncio
async def test_from_blueprint_export_import(async_client_db: AsyncClient):
    email = f"exp-{uuid.uuid4().hex[:8]}@example.com"
    reg = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"},
    )
    token = reg.json()["access_token"]

    payload = {
        "id": "custom-import-test",
        "tier": "basic",
        "name": "Imported blueprint",
        "tagline": "Test",
        "category": "test",
        "primaryRuntime": "python",
        "transport": "stdio",
        "overview": "O",
        "design": "D",
        "extensionIdeas": "",
        "risks": "",
        "suggestedTools": ["alpha", "beta"],
        "project_name": "Renamed on import",
    }
    r = await async_client_db.post(
        "/api/v1/projects/from-blueprint-export",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert r.status_code == 201, r.text
    assert r.json()["name"] == "Renamed on import"
