"""Auth routes: register, login, logout, me (docs/API_SPEC.md §2)."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse, UserLogin, UserPublic, UserRegister
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _error(code: str, message: str, status_code: int) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error": {"code": code, "message": message, "details": {}}},
    )


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    body: UserRegister,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    try:
        _user, token = await auth_service.register_user(db, body)
    except auth_service.AuthError as e:
        raise _error(e.code, e.message, e.status_code) from e
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
