"""Pytest configuration — env before importing the app, DB fixtures for auth tests."""

import os

os.environ.setdefault(
    "JWT_SECRET_KEY",
    "test-jwt-secret-key-must-be-at-least-32-bytes-long",
)
