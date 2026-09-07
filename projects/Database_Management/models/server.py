# ==============================================================================
# File        : models/server.py
# Location    : /data/database-management/models/server.py
# Purpose     : SQLAlchemy model for registered database servers (inventory records).
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from datetime import datetime

from . import db


class Server(db.Model):
    __tablename__ = "servers"

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(120), nullable=False, index=True)
    ip = db.Column(db.String(45), nullable=False)
    ssh_port = db.Column(db.Integer, default=22)
    db_port = db.Column(db.Integer, default=27017)
    db_type = db.Column(db.String(20), default="mongodb")  # mongodb | mssql | mysql | mariadb | postgresql

    environment = db.Column(db.String(10), default="DEV")  # DEV | TEST | UAT | PROD
    app_name = db.Column(db.String(150))
    app_owner = db.Column(db.String(120))
    server_owner = db.Column(db.String(120))

    os_type = db.Column(db.String(30), default="RHEL")
    os_version = db.Column(db.String(20))

    db_edition = db.Column(db.String(30))   # Community | Enterprise
    db_version = db.Column(db.String(30))
    replica_set = db.Column(db.String(80))
    replica_role = db.Column(db.String(20))  # PRIMARY | SECONDARY | ARBITER

    cpu_cores = db.Column(db.Integer)
    ram_gb = db.Column(db.Integer)
    storage_gb = db.Column(db.Integer)

    status = db.Column(db.String(20), default="unknown")  # online | offline | warning | unknown
    last_check = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    health_checks = db.relationship(
        "HealthCheck", backref="server", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "hostname": self.hostname,
            "ip": self.ip,
            "ssh_port": self.ssh_port,
            "db_port": self.db_port,
            "db_type": self.db_type,
            "environment": self.environment,
            "app_name": self.app_name,
            "app_owner": self.app_owner,
            "server_owner": self.server_owner,
            "os_type": self.os_type,
            "os_version": self.os_version,
            "db_edition": self.db_edition,
            "db_version": self.db_version,
            "replica_set": self.replica_set,
            "replica_role": self.replica_role,
            "cpu_cores": self.cpu_cores,
            "ram_gb": self.ram_gb,
            "storage_gb": self.storage_gb,
            "status": self.status,
            "last_check": self.last_check.strftime("%Y-%m-%d %H:%M:%S") if self.last_check else None,
        }
