# ==============================================================================
# File        : config.py
# Location    : /data/database-management/config.py
# Purpose     : Central configuration - reads all environment variables (PostgreSQL, MongoDB, SSH, session, scheduler) from .env.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

import os
from datetime import timedelta
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-in-production")

    # ---- PostgreSQL: the application's own repository ----
    # Stores: users, servers (inventory), health_checks, audit_logs
    PG_HOST = os.environ.get("PG_HOST", "localhost")
    PG_PORT = os.environ.get("PG_PORT", "5432")
    PG_DB = os.environ.get("PG_DB", "db_inventory")
    PG_USER = os.environ.get("PG_USER", "postgres")
    PG_PASSWORD = os.environ.get("PG_PASSWORD", "postgres")

    # quote_plus escapes special characters (@, :, /, etc.) so passwords like
    # "DBA@2026" don't break the connection URL's user:password@host parsing.
    _PG_USER_ENC = quote_plus(PG_USER)
    _PG_PASSWORD_ENC = quote_plus(PG_PASSWORD)

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{_PG_USER_ENC}:{_PG_PASSWORD_ENC}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---- MongoDB targets ----
    # Each row in `servers` carries its own ip/db_port, so the collector
    # connects per-server. This default is only used for local smoke tests.
    MONGO_DEFAULT_URI = os.environ.get("MONGO_DEFAULT_URI", "mongodb://localhost:27017")
    MONGO_CONNECT_TIMEOUT_MS = int(os.environ.get("MONGO_CONNECT_TIMEOUT_MS", 4000))

    # ---- Session / auth ----
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Set True once served over HTTPS
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() == "true"

    # ---- SSH collector (OS-level metrics) ----
    SSH_USERNAME = os.environ.get("SSH_USERNAME", "monitor")
    SSH_KEY_PATH = os.environ.get("SSH_KEY_PATH", "")  # empty -> falls back to agent/default key
    SSH_CONNECT_TIMEOUT = int(os.environ.get("SSH_CONNECT_TIMEOUT", 8))

    # ---- Background scheduler ----
    ENABLE_SCHEDULER = os.environ.get("ENABLE_SCHEDULER", "true").lower() == "true"
    HEALTHCHECK_INTERVAL_SECONDS = int(os.environ.get("HEALTHCHECK_INTERVAL_SECONDS", 60))

    # ---- Seed users (created on first run only, if `users` table is empty) ----
    DEFAULT_ADMIN_PASSWORD = os.environ.get("DEFAULT_ADMIN_PASSWORD", "admin123")
    DEFAULT_DBA_PASSWORD = os.environ.get("DEFAULT_DBA_PASSWORD", "dba123")
    DEFAULT_VIEWER_PASSWORD = os.environ.get("DEFAULT_VIEWER_PASSWORD", "viewer123")
