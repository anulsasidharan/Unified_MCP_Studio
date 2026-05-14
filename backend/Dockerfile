# API container (Cloud Run — docs/DEPLOYMENT.md)
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY entrypoint.sh ./

# psycopg2-binary is required by Alembic's sync migration runner (asyncpg is runtime-only)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir . psycopg2-binary \
    && chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
