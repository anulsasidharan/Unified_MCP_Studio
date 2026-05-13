"""Liveness for versioned API surface (orchestrators may probe /api/v1/health)."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="API v1 health")
def api_v1_health() -> dict[str, str]:
    return {"status": "ok", "api_version": "v1"}
