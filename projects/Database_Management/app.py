# ==============================================================================
# File        : app.py
# Location    : /data/database-management/app.py
# Purpose     : Flask application factory - registers blueprints, initializes SQLAlchemy, CORS, and the background scheduler.
# Author      : Madan U
# Email       : madan.u@kotak.com
# Created On  : 2026-09-07
# Last Update : 2026-09-07
# ==============================================================================

import os

from dotenv import load_dotenv

load_dotenv()  # reads .env if present, before Config reads os.environ

from flask import Flask
from flask_cors import CORS

from config import Config
from models import db
from models.user import User


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="",       # so ./css/styles.css, ./js/app.js resolve at site root
        template_folder="templates",
    )
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    from routes.auth_routes import auth_bp
    from routes.health_routes import health_bp
    from routes.page_routes import pages_bp
    from routes.server_routes import api_servers_bp
    from routes.user_routes import users_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_servers_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(health_bp)

    with app.app_context():
        db.create_all()
        _seed_default_users(app)

    if app.config.get("ENABLE_SCHEDULER", True) and not app.config.get("TESTING"):
        _start_scheduler(app)

    return app


def _seed_default_users(app):
    """Creates admin/dba/viewer accounts on first run only (table empty)."""
    if User.query.first():
        return
    admin = User(username="admin", name="Admin User", role="Admin")
    admin.set_password(app.config["DEFAULT_ADMIN_PASSWORD"])
    db.session.add(admin)

    dba = User(username="dba", name="DBA User", role="DBA")
    dba.set_password(app.config["DEFAULT_DBA_PASSWORD"])
    db.session.add(dba)

    viewer = User(username="viewer", name="Viewer User", role="Viewer")
    viewer.set_password(app.config["DEFAULT_VIEWER_PASSWORD"])
    db.session.add(viewer)

    db.session.commit()
    app.logger.info("Seeded default users: admin, dba, viewer (change these passwords).")


def _start_scheduler(app):
    from apscheduler.schedulers.background import BackgroundScheduler
    from services.monitoring_service import sweep_all_servers

    scheduler = BackgroundScheduler(daemon=True)

    def job():
        with app.app_context():
            sweep_all_servers()

    scheduler.add_job(job, "interval", seconds=app.config["HEALTHCHECK_INTERVAL_SECONDS"])
    scheduler.start()
    app.logger.info(f"Health-check scheduler started (every {app.config['HEALTHCHECK_INTERVAL_SECONDS']}s).")


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "true").lower() == "true")
