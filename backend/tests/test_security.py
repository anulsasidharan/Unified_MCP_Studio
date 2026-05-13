"""Unit tests for password hashing and JWT (no database)."""

import uuid

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_roundtrip():
    h = hash_password("correct horse battery staple")
    assert verify_password("correct horse battery staple", h)
    assert not verify_password("wrong", h)


def test_jwt_roundtrip():
    uid = uuid.uuid4()
    token = create_access_token(uid)
    payload = decode_access_token(token)
    assert payload["sub"] == str(uid)
