"""Auth routes: register, login, logout, me (docs/API_SPEC.md §2)."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserPublic, UserRegister
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

_DB_UNAVAILABLE_MSG = (
    "Cannot reach PostgreSQL. Ensure the server is running (e.g. `docker compose up -d postgres` "
    "from the repo root). If the API runs on your machine, use host `127.0.0.1` and the published "
    "port (default 5432, or POSTGRES_PORT from compose). If the API runs inside Docker on the "
    "same compose network, use host `postgres` (the service name). Verify DATABASE_URL user, "
    "password, and database match POSTGRES_USER, POSTGRES_PASSWORD, and POSTGRES_DB."
)


def _error(code: str, message: str, status_code: int) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error": {"code": code, "message": message, "details": {}}},
    )


def _is_async_db_driver_error(exc: BaseException) -> bool:
    """asyncpg errors can propagate without a SQLAlchemy wrapper from async engine code."""
    return type(exc).__module__.startswith("asyncpg")


def _raise_database_unavailable(log_event: str) -> None:
    logger.exception(log_event)
    raise _error(
        "DATABASE_UNAVAILABLE",
        _DB_UNAVAILABLE_MSG,
        status.HTTP_503_SERVICE_UNAVAILABLE,
    ) from None


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserRegister,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    try:
        _user, token = await auth_service.register_user(db, body)
    except auth_service.AuthError as e:
        raise _error(e.code, e.message, e.status_code) from e
    except SQLAlchemyError:
        _raise_database_unavailable("auth_register_database_error")
    except Exception as exc:
        if _is_async_db_driver_error(exc):
            _raise_database_unavailable("auth_register_database_error")
        raise
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(
    body: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    try:
        _user, token = await auth_service.authenticate(db, body)
    except auth_service.AuthError as e:
        raise _error(e.code, e.message, e.status_code) from e
    except SQLAlchemyError:
        _raise_database_unavailable("auth_login_database_error")
    except Exception as exc:
        if _is_async_db_driver_error(exc):
            _raise_database_unavailable("auth_login_database_error")
        raise
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    _user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Stateless JWT: client discards token; revocation can be added later (e.g. Redis)."""
    return None


@router.get("/me", response_model=UserPublic)
async def me(current: Annotated[User, Depends(get_current_user)]) -> User:
    return current
