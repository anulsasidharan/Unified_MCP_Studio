"""Celery application."""

from celery import Celery

from app.config import settings

celery_app = Celery(
    "mcpstudio",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.workers.tasks.codegen_bundle": {"queue": "codegen"},
        "app.workers.tasks.deploy_cloud_run": {"queue": "deploy"},
    },
)

# Register tasks
from app.workers import tasks  # noqa: E402,F401
