"""Celery tasks."""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from app.db.session import AsyncSessionLocal
from app.models.deployment import Deployment
from app.services import codegen_service
from app.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.tasks.codegen_bundle")
def codegen_bundle(project_id: str) -> dict[str, Any]:
    pid = uuid.UUID(project_id)

    async def _run() -> dict[str, Any]:
        async with AsyncSessionLocal() as db:
            return await codegen_service.write_zip_artifact(db, pid)

    return asyncio.run(_run())


@celery_app.task(name="app.workers.tasks.deploy_cloud_run")
def deploy_cloud_run(deployment_id: str) -> dict[str, Any]:
    """Placeholder Cloud Run deploy — records outcome without calling gcloud (Phase 7)."""

    did = uuid.UUID(deployment_id)

    async def _run() -> dict[str, Any]:
        async with AsyncSessionLocal() as db:
            row = await db.get(Deployment, did)
            if row is None:
                return {"ok": False, "error": "deployment not found"}
            row.status = "failed"
            row.error_message = (
                "Cloud Run deploy integration not configured in this environment "
                "(set GCP credentials + worker image per docs/DEPLOYMENT.md)."
            )
            await db.commit()
            logger.warning("deploy_cloud_run_stub", extra={"deployment_id": deployment_id})
            return {"ok": True, "status": row.status}

    return asyncio.run(_run())


@celery_app.task(name="app.workers.tasks.mark_deployment_pending")
def noop() -> None:
    """Reserved for future routing hooks."""
    return None
