# ==============================================================================
# File        : services/inventory_service.py
# Location    : /data/database-management/services/inventory_service.py
# Purpose     : Business logic layer for server inventory - orchestrates collector calls and persistence.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from datetime import datetime

from models import db
from models.metrics import AuditLog
from models.server import Server

SERVER_EDITABLE_FIELDS = [
    "hostname", "ip", "ssh_port", "db_port", "db_type", "environment",
    "app_name", "app_owner", "server_owner", "os_type", "os_version",
    "db_edition", "db_version", "replica_set", "replica_role",
    "cpu_cores", "ram_gb", "storage_gb",
]


def list_servers(environment=None, db_type=None):
    q = Server.query
    if environment:
        q = q.filter_by(environment=environment)
    if db_type:
        q = q.filter_by(db_type=db_type)
    return q.order_by(Server.hostname.asc()).all()


def get_server(server_id):
    return Server.query.get(server_id)


def add_server(data, actor_username=None):
    server = Server(
        hostname=data.get("hostname"),
        ip=data.get("ip"),
        ssh_port=data.get("ssh_port", 22),
        db_port=data.get("db_port", 27017),
        db_type=data.get("db_type", "mongodb"),
        environment=data.get("environment", "DEV"),
        app_name=data.get("app_name"),
        app_owner=data.get("app_owner"),
        server_owner=data.get("server_owner"),
        os_type=data.get("os_type", "RHEL"),
        os_version=data.get("os_version"),
        db_edition=data.get("db_edition"),
        db_version=data.get("db_version"),
        replica_set=data.get("replica_set"),
        replica_role=data.get("replica_role"),
        cpu_cores=data.get("cpu_cores"),
        ram_gb=data.get("ram_gb"),
        storage_gb=data.get("storage_gb"),
        status="unknown",
        last_check=None,
    )
    db.session.add(server)
    db.session.commit()
    _audit(actor_username, "ADD_SERVER", server.hostname)
    return server


def update_server(server_id, data, actor_username=None):
    server = Server.query.get(server_id)
    if not server:
        return None
    for field in SERVER_EDITABLE_FIELDS:
        if field in data:
            setattr(server, field, data[field])
    server.updated_at = datetime.utcnow()
    db.session.commit()
    _audit(actor_username, "EDIT_SERVER", server.hostname)
    return server


def delete_server(server_id, actor_username=None):
    server = Server.query.get(server_id)
    if not server:
        return False
    hostname = server.hostname
    db.session.delete(server)
    db.session.commit()
    _audit(actor_username, "DELETE_SERVER", hostname)
    return True


def _audit(username, action, target, details=None):
    if not username:
        return
    db.session.add(AuditLog(username=username, action=action, target=target, details=details))
    db.session.commit()
