# ==============================================================================
# File        : routes/user_routes.py
# Location    : /data/database-management/routes/user_routes.py
# Purpose     : User management routes - create, update, and manage application user accounts.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from functools import wraps

from flask import Blueprint, jsonify, request, session

from models import db
from models.user import ROLES, User

users_bp = Blueprint("api_users", __name__, url_prefix="/api/users")


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get("role") != "Admin":
            return jsonify({"error": "Admin privileges required."}), 403
        return fn(*args, **kwargs)
    return wrapper


@users_bp.route("", methods=["GET"])
@admin_required
def list_users():
    users = User.query.order_by(User.username.asc()).all()
    return jsonify([u.to_dict() for u in users])


@users_bp.route("", methods=["POST"])
@admin_required
def create_user():
    data = request.get_json(force=True) or {}
    username = (data.get("username") or "").strip().lower()
    name = (data.get("name") or "").strip()
    password = data.get("password") or ""
    role = data.get("role", "Viewer")

    if not username or not name or not password:
        return jsonify({"error": "username, name and password are required."}), 400
    if role not in ROLES:
        return jsonify({"error": f"role must be one of {ROLES}."}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 409

    user = User(username=username, name=name, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
@admin_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    data = request.get_json(force=True) or {}

    if "name" in data:
        user.name = data["name"]
    if "role" in data:
        if data["role"] not in ROLES:
            return jsonify({"error": f"role must be one of {ROLES}."}), 400
        user.role = data["role"]
    if "is_active" in data:
        user.is_active = bool(data["is_active"])
    if data.get("password"):
        user.set_password(data["password"])

    db.session.commit()
    return jsonify(user.to_dict())


@users_bp.route("/<int:user_id>", methods=["DELETE"])
@admin_required
def remove_user(user_id):
    if session.get("user_id") == user_id:
        return jsonify({"error": "You cannot delete your own account while logged in."}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"deleted": True})
