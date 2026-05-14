#!/bin/sh
set -e

# Guard against a stale alembic_version stamp: if the version table claims we
# are already at head but the 'users' table is missing, the stamp was written
# without the DDL ever running.  Reset it so the upgrade runs from scratch.
python - <<'EOF'
import os, sys
try:
    import psycopg2
    url = os.environ.get("DATABASE_URL", "").replace("+asyncpg", "")
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute(
        "SELECT EXISTS ("
        "  SELECT FROM pg_tables"
        "  WHERE schemaname = 'public' AND tablename = 'users'"
        ")"
    )
    users_exists = cur.fetchone()[0]
    if not users_exists:
        cur.execute("DELETE FROM alembic_version")
        conn.commit()
        print("[entrypoint] alembic_version stamp cleared — tables were missing, will run full upgrade")
    else:
        print("[entrypoint] tables present, alembic will apply any pending migrations")
    conn.close()
except Exception as exc:
    print(f"[entrypoint] pre-check skipped ({exc}), proceeding with upgrade")
EOF

alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
