"""User registration and authentication."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister


class AuthError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def register_user(db: AsyncSession, body: UserRegister) -> tuple[User, str]:
    cleaned_name = body.name.strip() if body.name and body.name.strip() else None
    user = User(
        email=body.email.lower().strip(),
        password_hash=hash_password(body.password),
        name=cleaned_name,
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise AuthError(
            "EMAIL_TAKEN",
            "An account with this email already exists.",
            status_code=409,
        ) from exc
    except SQLAlchemyError as exc:
        await db.rollback()
        hint = (
            "Check that PostgreSQL is running "
            "(e.g. docker compose up -d postgres from the repo root), "
            "DATABASE_URL in backend/.env matches it, and migrations are applied: "
            "cd backend && alembic upgrade head."
        )
        detail = f"{hint} ({type(exc).__name__}: {exc})" if settings.debug else hint
        raise AuthError("DB_UNAVAILABLE", detail, status_code=503) from exc
    await db.refresh(user)
    token = create_access_token(user.id)
    return user, token


async def authenticate(db: AsyncSession, body: UserLogin) -> tuple[User, str]:
    result = await db.execute(select(User).where(User.email == body.email.lower().strip()))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(body.password, user.password_hash):
        raise AuthError(
            "INVALID_CREDENTIALS",
            "Incorrect email or password.",
            status_code=401,
        )
    token = create_access_token(user.id)
    return user, token
