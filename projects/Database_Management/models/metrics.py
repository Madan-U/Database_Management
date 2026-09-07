# ==============================================================================
# File        : models/metrics.py
# Location    : /data/database-management/models/metrics.py
# Purpose     : SQLAlchemy model for stored health-check / metrics history.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from datetime import datetime
from app import db


class HealthCheck(db.Model):
    __tablename__ = "health_checks"

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False, index=True)
    check_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    status = db.Column(db.String(20))  # green | yellow | red | gray
    cpu_usage = db.Column(db.Float)
    memory_usage = db.Column(db.Float)
    disk_usage = db.Column(db.Float)

    mongo_status = db.Column(db.String(20))     # running | down | unreachable | unknown
    replica_role = db.Column(db.String(20))
    replication_lag = db.Column(db.Float)
    connections_used = db.Column(db.Integer)

    remarks = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "server_id": self.server_id,
            "check_time": self.check_time.strftime("%Y-%m-%d %H:%M:%S") if self.check_time else None,
            "status": self.status,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "disk_usage": self.disk_usage,
            "mongo_status": self.mongo_status,
            "replica_role": self.replica_role,
            "replication_lag": self.replication_lag,
            "connections_used": self.connections_used,
            "remarks": self.remarks,
        }


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.String(80))
    action = db.Column(db.String(50))       # LOGIN, LOGIN_FAILED, LOGOUT, ADD_SERVER, EDIT_SERVER, DELETE_SERVER, ADD_USER, ...
    target = db.Column(db.String(150))
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "action": self.action,
            "target": self.target,
            "details": self.details,
            "ip_address": self.ip_address,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
