"""Pytest configuration — env before importing the app, DB fixtures for API tests."""

import os
import uuid

os.environ.setdefault(
    "JWT_SECRET_KEY",
    "test-jwt-secret-key-must-be-at-least-32-bytes-long",
)

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.session import get_db
from app.main import app
from app.models.base import Base
from app.models.library_template import LibraryTemplate

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://mcpstudio:mcpstudio@127.0.0.1:5432/mcpstudio",
    ),
)

SEED_LIBRARY_TEMPLATE_ID = uuid.UUID("00000000-0000-0000-0000-00000000ab00")


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

    async with session_factory() as session:
        session.add(
            LibraryTemplate(
                id=SEED_LIBRARY_TEMPLATE_ID,
                name="Seed REST",
                description="Minimal template for tests",
                category="api",
                is_public=True,
                author_id=None,
                use_count=0,
                config={
                    "runtime": "python",
                    "transport": "stdio",
                    "tools": [
                        {
                            "name": "ping",
                            "description": "Health check",
                            "input_schema": {"type": "object", "properties": {}},
                            "handler_code": "return 'pong'",
                            "handler_language": "python",
                        }
                    ],
                },
            )
        )
        await session.commit()

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
