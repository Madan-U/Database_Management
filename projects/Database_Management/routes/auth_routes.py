# ==============================================================================
# File        : routes/auth_routes.py
# Location    : /data/database-management/routes/auth_routes.py
# Purpose     : Authentication routes - login, logout, and session handling.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from datetime import datetime

from flask import Blueprint, jsonify, request, session

from models import db
from models.metrics import AuditLog
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True) or {}
    username = (data.get("username") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(username=username, is_active=True).first()
    if not user or not user.check_password(password):
        db.session.add(AuditLog(username=username, action="LOGIN_FAILED", target=username,
                                 ip_address=request.remote_addr))
        db.session.commit()
        return jsonify({"error": "Invalid username or password."}), 401

    session.clear()
    session.permanent = True
    session["user_id"] = user.id
    session["username"] = user.username
    session["role"] = user.role
    session["name"] = user.name

    user.last_login = datetime.utcnow()
    db.session.add(AuditLog(user_id=user.id, username=user.username, action="LOGIN",
                             target=user.username, ip_address=request.remote_addr))
    db.session.commit()

    return jsonify(user.to_dict())


@auth_bp.route("/logout", methods=["POST"])
def logout():
    username = session.get("username")
    if username:
        db.session.add(AuditLog(username=username, action="LOGOUT", target=username,
                                 ip_address=request.remote_addr))
        db.session.commit()
    session.clear()
    return jsonify({"ok": True})


@auth_bp.route("/me", methods=["GET"])
def me():
    if "user_id" not in session:
        return jsonify(None), 200
    return jsonify({
        "id": session["user_id"],
        "username": session["username"],
        "role": session["role"],
        "name": session["name"],
    })
