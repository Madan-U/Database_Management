-- ==============================================================================
-- File        : schema.sql
-- Location    : /data/database-management/schema.sql
-- Purpose     : PostgreSQL DDL - creates the users, servers, health_checks and related tables for the Database Management Console repository.
-- Author      : Madan U
-- Email       : madan.u@kotak.com
-- Created On  : 2026-09-07
-- Last Update : 2026-09-07
-- ==============================================================================

-- Manual reference schema for PostgreSQL.
-- NOT required to run manually — app.py calls db.create_all() on startup
-- and creates these tables automatically if they don't exist. Use this only
-- if you prefer to provision the schema yourself (e.g. via a DBA change
-- ticket) before first app startup.

CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(80) UNIQUE NOT NULL,
    name          VARCHAR(120) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(20) NOT NULL DEFAULT 'Viewer',   -- Admin | DBA | Viewer
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    last_login    TIMESTAMP,
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS servers (
    id            SERIAL PRIMARY KEY,
    hostname      VARCHAR(120) NOT NULL,
    ip            VARCHAR(45) NOT NULL,
    ssh_port      INTEGER DEFAULT 22,
    db_port       INTEGER DEFAULT 27017,
    db_type       VARCHAR(20) DEFAULT 'mongodb',
    environment   VARCHAR(10) DEFAULT 'DEV',               -- DEV | TEST | UAT | PROD
    app_name      VARCHAR(150),
    app_owner     VARCHAR(120),
    server_owner  VARCHAR(120),
    os_type       VARCHAR(30) DEFAULT 'RHEL',
    os_version    VARCHAR(20),
    db_edition    VARCHAR(30),
    db_version    VARCHAR(30),
    replica_set   VARCHAR(80),
    replica_role  VARCHAR(20),                             -- PRIMARY | SECONDARY | ARBITER
    cpu_cores     INTEGER,
    ram_gb        INTEGER,
    storage_gb    INTEGER,
    status        VARCHAR(20) DEFAULT 'unknown',            -- online | offline | warning | unknown
    last_check    TIMESTAMP,
    created_at    TIMESTAMP DEFAULT NOW(),
    updated_at    TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_servers_hostname ON servers (hostname);

CREATE TABLE IF NOT EXISTS health_checks (
    id                SERIAL PRIMARY KEY,
    server_id         INTEGER NOT NULL REFERENCES servers(id) ON DELETE CASCADE,
    check_time        TIMESTAMP DEFAULT NOW(),
    status            VARCHAR(20),                          -- green | yellow | red | gray
    cpu_usage         FLOAT,
    memory_usage      FLOAT,
    disk_usage        FLOAT,
    mongo_status      VARCHAR(20),
    replica_role      VARCHAR(20),
    replication_lag   FLOAT,
    connections_used  INTEGER,
    remarks           TEXT
);

CREATE INDEX IF NOT EXISTS idx_health_checks_server_time ON health_checks (server_id, check_time DESC);

CREATE TABLE IF NOT EXISTS audit_logs (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER REFERENCES users(id),
    username    VARCHAR(80),
    action      VARCHAR(50),
    target      VARCHAR(150),
    details     TEXT,
    ip_address  VARCHAR(45),
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs (created_at DESC);
