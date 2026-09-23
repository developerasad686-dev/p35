"""Vercel build hook for Django (see [tool.vercel.scripts] in pyproject.toml).

Runs `python manage.py migrate` during the Vercel build step, after
dependencies are installed and before Vercel packages the deployment.
Vercel injects the project's configured environment variables (for the
target environment, e.g. Production) into this build step, so the
database is reachable here even though it is not reachable from local
sandboxed tooling.

Migrations are run against a non-pooled connection when one is available
(DATABASE_URL_UNPOOLED for Neon, DATABASE_POSTGRES_URL_NON_POOLING for the
Supabase Vercel integration) because DDL statements inside Django's
migration transactions can be unreliable through a transaction-mode
connection pooler (PgBouncer/Supavisor). The app's runtime settings.py
still uses the pooled URL for normal request traffic.
"""

import os
import subprocess
import sys

# Preference order: unpooled/direct connection first (safe for DDL),
# then whatever pooled URL the integration provided.
_CANDIDATE_ENV_VARS = (
    "DATABASE_URL_UNPOOLED",              # Neon
    "DATABASE_POSTGRES_URL_NON_POOLING",  # Supabase (Vercel integration, prefix=DATABASE)
    "DATABASE_URL",                       # Neon (pooled) / generic
    "DATABASE_POSTGRES_URL",              # Supabase (pooled)
    "POSTGRES_URL",                       # Generic Vercel Postgres naming
)


def _resolve_migration_database_url():
    for key in _CANDIDATE_ENV_VARS:
        value = os.environ.get(key)
        if value:
            print(f"build.py: using {key} for migrations")
            return value
    return None


def main():
    env = os.environ.copy()
    database_url = _resolve_migration_database_url()

    if database_url is None:
        print(
            "build.py: no DATABASE_URL-like environment variable found; "
            "skipping migrate (settings.py will fall back to sqlite, which "
            "is not persisted between deployments)."
        )
        return

    # Normalize onto DATABASE_URL so settings.py's single lookup picks it up,
    # regardless of which provider-specific name it came from.
    env["DATABASE_URL"] = database_url

    print("build.py: running python manage.py migrate --noinput")
    subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        check=True,
        env=env,
    )
    print("build.py: migrations complete")


if __name__ == "__main__":
    main()
