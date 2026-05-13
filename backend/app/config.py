"""Environment-based settings (GCP Secret Manager in production — docs/DEPLOYMENT.md)."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Unified MCP Studio API"
    environment: str = "development"
    debug: bool = False

    api_v1_prefix: str = "/api/v1"

    # Comma-separated origins, e.g. "http://localhost:3000,https://app.example.com"
    # Include 127.0.0.1 — browsers treat it as a different origin than "localhost".
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    database_url: str = "postgresql+asyncpg://mcpstudio:mcpstudio@127.0.0.1:5432/mcpstudio"
    redis_url: str = "redis://127.0.0.1:6379/0"
    celery_broker_url: str = "redis://127.0.0.1:6379/1"
    celery_result_backend: str = "redis://127.0.0.1:6379/2"

    # JWT (use Secret Manager / strong random value in production — docs/DEPLOYMENT.md)
    jwt_secret_key: str = Field(
        default="dev-only-change-me-use-openssl-rand-hex-32-chars-min",
        min_length=32,
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days; tune per product policy

    # Codegen / artifacts (Phase 4 — docs/DEPLOYMENT.md for GCS in prod)
    # Empty → resolve relative to monorepo `templates/`.
    codegen_template_root: str = ""
    artifact_local_dir: str = "./var/artifacts"
    gcs_bucket: str = ""  # set for signed URLs; optional dependency unified-mcp-studio-api[gcp]
    gcs_sign_ttl_seconds: int = 3600
    # True requires Redis + Celery worker on the `codegen` queue.
    codegen_use_celery: bool = False

    # Sandbox (Phase 5)
    sandbox_workspace_root: str = "./var/sandbox"
    sandbox_subprocess_timeout_seconds: int = 60
    sandbox_max_output_bytes: int = 256_000

    # Deploy worker (Phase 7)
    gcp_project_id: str = ""
    gcp_region: str = "us-central1"
    cloud_run_service_name: str = ""

    # Optional Claude proxy (Phase 5 optional task)
    anthropic_api_key: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        origins = [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        if not origins and self.environment == "development":
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        return origins


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
