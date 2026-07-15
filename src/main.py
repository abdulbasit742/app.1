import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from src.config import load_config
from src.models.user import User, db
from src.routes.announcement import announcement_bp
from src.routes.auth import auth_bp
from src.routes.contact import contact_bp
from src.routes.product import product_bp
from src.routes.service import service_bp
from src.routes.user import user_bp


def _bootstrap_admin(app):
    bootstrap = app.config.get("BOOTSTRAP_ADMIN")
    if not bootstrap or User.query.filter_by(email=bootstrap["email"]).first():
        return
    admin = User(name=bootstrap["name"], email=bootstrap["email"], role="admin", phone="", skills="", achievements="")
    admin.set_password(bootstrap["password"])
    db.session.add(admin)
    db.session.commit()
    app.logger.warning("Bootstrap administrator created for %s; remove bootstrap credentials from the environment", bootstrap["email"])


def create_app(test_config=None):
    static_folder = Path(__file__).parent / "static"
    app = Flask(__name__, static_folder=str(static_folder), instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_mapping(load_config(app.instance_path, test_config))

    CORS(app, resources={r"/api/*": {"origins": list(app.config["CORS_ORIGINS"])}}, supports_credentials=True)
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(service_bp, url_prefix="/api")
    app.register_blueprint(announcement_bp, url_prefix="/api")
    app.register_blueprint(contact_bp, url_prefix="/api")

    @app.before_request
    def protect_cookie_mutations():
        if request.path.startswith("/api/") and request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 415
            origin = request.headers.get("Origin")
            if origin and origin not in app.config["CORS_ORIGINS"]:
                return jsonify({"error": "Origin is not allowed"}), 403
        return None

    @app.after_request
    def security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        response.headers.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        if request.path.startswith("/api/"):
            response.headers.setdefault("Cache-Control", "no-store")
        return response

    @app.get("/api/health")
    def health_check():
        return {"status": "healthy", "service": "pes-api"}, 200

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path and (static_folder / path).is_file():
            return send_from_directory(static_folder, path)
        if (static_folder / "index.html").is_file():
            return send_from_directory(static_folder, "index.html")
        return "index.html not found", 404

    with app.app_context():
        db.create_all()
        _bootstrap_admin(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host=os.getenv("BIND_HOST", "127.0.0.1"), port=int(os.getenv("PORT", "5000")), debug=os.getenv("FLASK_DEBUG") == "1")
