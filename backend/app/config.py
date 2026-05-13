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
    cors_origins: str = "http://localhost:3000"

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

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
