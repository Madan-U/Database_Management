# ==============================================================================
# File        : services/monitoring_service.py
# Location    : /data/database-management/services/monitoring_service.py
# Purpose     : Business logic layer for health monitoring - aggregates health-check results for the dashboard.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from datetime import datetime
from models import db
from models.metrics import HealthCheck
from models.server import Server
from collectors.mongodb_collector import run_mongo_health_check
from collectors.ssh_collector import collect_os_metrics

def run_health_check(server_id):
    """Runs OS (SSH) + MongoDB checks for one server, stores a HealthCheck
    row, and updates the server's cached status/last_check/replica_role."""
    server = Server.query.get(server_id)
    if not server:
        return None

    os_metrics = collect_os_metrics(server)
    mongo_result = run_mongo_health_check(server)

    # Worst-of-both status: red > yellow > gray > green
    severity = {"red": 3, "yellow": 2, "gray": 1, "green": 0}
    overall = max([os_metrics.get("status", "green"), mongo_result.get("status", "green")], key=lambda s: severity.get(s, 0))

    hc = HealthCheck(
        server_id=server.id,
        status=overall,
        cpu_usage=os_metrics.get("cpu_usage"),
        memory_usage=os_metrics.get("memory_usage"),
        disk_usage=os_metrics.get("disk_usage"),
        mongo_status=mongo_result.get("mongod_status") or mongo_result.get("mongo_status"),
        replica_role=mongo_result.get("replica_role"),
        replication_lag=mongo_result.get("replication_lag"),
        connections_used=mongo_result.get("connections_used"),
        remarks=mongo_result.get("remarks"),
    )
    db.session.add(hc)

    if overall == "red":
        server.status = "offline"
    elif overall == "yellow":
        server.status = "warning"
    elif overall == "green":
        server.status = "online"

    server.last_check = datetime.utcnow()
    if mongo_result.get("replica_role"):
        server.replica_role = mongo_result["replica_role"]

    db.session.commit()
    return hc

def sweep_all_servers():
    """Called by APScheduler on HEALTHCHECK_INTERVAL_SECONDS."""
    from flask import current_app
    results = []
    for server in Server.query.all():
        try:
            results.append(run_health_check(server.id))
        except Exception as e:
            current_app.logger.error(f"Health check failed for {server.hostname}: {e}")
    return results
