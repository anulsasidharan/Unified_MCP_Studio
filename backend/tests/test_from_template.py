"""POST /api/v1/projects/from-template integration tests."""

import uuid

import pytest
from httpx import AsyncClient

from tests.conftest import SEED_LIBRARY_TEMPLATE_ID


@pytest.mark.asyncio
async def test_from_template_requires_auth(async_client_db: AsyncClient):
    r = await async_client_db.post(
        "/api/v1/projects/from-template",
        json={"template_id": str(SEED_LIBRARY_TEMPLATE_ID)},
    )
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_from_template_unknown_template(async_client_db: AsyncClient):
    email = f"tpl-{uuid.uuid4().hex[:8]}@example.com"
    reg = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"},
    )
    token = reg.json()["access_token"]
    missing = uuid.uuid4()
    r = await async_client_db.post(
        "/api/v1/projects/from-template",
        headers={"Authorization": f"Bearer {token}"},
        json={"template_id": str(missing)},
    )
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_from_template_creates_project_and_tools(async_client_db: AsyncClient):
    email = f"tpl-{uuid.uuid4().hex[:8]}@example.com"
    reg = await async_client_db.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "password123"},
    )
    token = reg.json()["access_token"]

    r = await async_client_db.post(
        "/api/v1/projects/from-template",
        headers={"Authorization": f"Bearer {token}"},
        json={"template_id": str(SEED_LIBRARY_TEMPLATE_ID), "name": "From seed"},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["name"] == "From seed"
    assert body["runtime"] == "python"
    assert body["transport"] == "stdio"
    pid = body["id"]

    tools = await async_client_db.get(
        f"/api/v1/projects/{pid}/tools",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert tools.status_code == 200
    listed = tools.json()
    assert len(listed) == 1
    assert listed[0]["name"] == "ping"
