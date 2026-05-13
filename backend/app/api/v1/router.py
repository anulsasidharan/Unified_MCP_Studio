"""Aggregate `/api/v1` routes."""

from fastapi import APIRouter

from app.api.v1 import (
    auth,
    deployments_route,
    health,
    projects,
    prompts_api,
    resources_api,
    templates_route,
    testing_api,
    tools_api,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(tools_api.proj_router)
api_router.include_router(tools_api.id_router)
api_router.include_router(resources_api.proj_router)
api_router.include_router(resources_api.id_router)
api_router.include_router(prompts_api.proj_router)
api_router.include_router(prompts_api.id_router)
api_router.include_router(templates_route.router)
api_router.include_router(deployments_route.router)
api_router.include_router(testing_api.router)
