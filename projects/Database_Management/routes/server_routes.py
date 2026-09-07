# ==============================================================================
# File        : routes/server_routes.py
# Location    : /data/database-management/routes/server_routes.py
# Purpose     : Server inventory CRUD routes - add, update, delete, list registered database servers.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from functools import wraps

from flask import Blueprint, jsonify, request, session

from services.inventory_service import add_server, delete_server, get_server, list_servers, update_server

api_servers_bp = Blueprint("api_servers", __name__, url_prefix="/api/servers")


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required."}), 401
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "Admin":
            return jsonify({"error": "Admin privileges required."}), 403
        return fn(*args, **kwargs)
    return wrapper


@api_servers_bp.route("", methods=["GET"])
@login_required
def get_servers():
    """Admin, DBA, and Viewer can all read the inventory."""
    environment = request.args.get("environment")
    db_type = request.args.get("db_type")
    servers = list_servers(environment=environment, db_type=db_type)
    return jsonify([s.to_dict() for s in servers])


@api_servers_bp.route("/<int:server_id>", methods=["GET"])
@login_required
def get_one_server(server_id):
    server = get_server(server_id)
    if not server:
        return jsonify({"error": "Server not found."}), 404
    return jsonify(server.to_dict())


@api_servers_bp.route("", methods=["POST"])
@admin_required
def create_server():
    data = request.get_json(force=True) or {}
    missing = [f for f in ("hostname", "ip", "app_name") if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    server = add_server(data, actor_username=session.get("username"))
    return jsonify(server.to_dict()), 201


@api_servers_bp.route("/<int:server_id>", methods=["PUT"])
@admin_required
def edit_server(server_id):
    data = request.get_json(force=True) or {}
    server = update_server(server_id, data, actor_username=session.get("username"))
    if not server:
        return jsonify({"error": "Server not found."}), 404
    return jsonify(server.to_dict())


@api_servers_bp.route("/<int:server_id>", methods=["DELETE"])
@admin_required
def remove_server(server_id):
    ok = delete_server(server_id, actor_username=session.get("username"))
    if not ok:
        return jsonify({"error": "Server not found."}), 404
    return jsonify({"deleted": True})
