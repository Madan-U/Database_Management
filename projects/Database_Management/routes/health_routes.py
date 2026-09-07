# ==============================================================================
# File        : routes/health_routes.py
# Location    : /data/database-management/routes/health_routes.py
# Purpose     : Health-check API routes - exposes live health/status data for registered servers.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from functools import wraps
from flask import Blueprint, jsonify, session
from models.metrics import HealthCheck
from services.monitoring_service import run_health_check

health_bp = Blueprint("api_health", __name__, url_prefix="/api")

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required."}), 401
        return fn(*args, **kwargs)
    return wrapper

@health_bp.route("/servers/<int:server_id>/health", methods=["GET"])
@login_required
def get_latest_health(server_id):
    """Returns the latest health check metrics for the server."""
    hc = HealthCheck.query.filter_by(server_id=server_id).order_by(HealthCheck.check_time.desc()).first()
    if not hc:
        return jsonify({"status": "gray", "cpu_usage": 0, "memory_usage": 0, "disk_usage": 0, "remarks": "No checks yet"}), 200
    return jsonify(hc.to_dict())

@health_bp.route("/servers/<int:server_id>/health-check", methods=["POST"])
@login_required
def trigger_health_check(server_id):
    hc = run_health_check(server_id)
    if not hc:
        return jsonify({"error": "Server not found."}), 404
    return jsonify(hc.to_dict())

@health_bp.route("/servers/<int:server_id>/health-checks", methods=["GET"])
@login_required
def get_health_history(server_id):
    checks = (
        HealthCheck.query.filter_by(server_id=server_id)
        .order_by(HealthCheck.check_time.desc())
        .limit(50)
        .all()
    )
    return jsonify([c.to_dict() for c in checks])
