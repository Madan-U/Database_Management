# ==============================================================================
# File        : routes/page_routes.py
# Location    : /data/database-management/routes/page_routes.py
# Purpose     : Page-rendering routes - serves the HTML templates (dashboard, inventory pages).
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

from flask import render_template
from flask import Blueprint

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
@pages_bp.route("/index.html")
def index():
    return render_template("index.html")


@pages_bp.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")


@pages_bp.route("/mongodb_inventory.html")
def mongodb_inventory():
    return render_template("mongodb_inventory.html")


@pages_bp.route("/server_detail.html")
def server_detail():
    # server id comes from the ?id= query string, read client-side by app.js
    return render_template("server_detail.html")
