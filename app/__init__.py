from flask import Flask, jsonify
from .config import get_config
from .extensions import db, migrate, ma, jwt
from .routes.auth import auth_bp
from .routes.items import items_bp

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)

    # blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(items_bp, url_prefix="/api/items")

    @app.route("/api/health")
    def health():
        return jsonify(status="ok")

    # Errors -> JSON
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Not found"), 404

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error="Bad request"), 400

    @app.errorhandler(422)
    def unprocessable(e):
        # Marshmallow validation errors come here sometimes
        messages = getattr(e, "data", {}).get("messages", None)
        return jsonify(error="Validation error", messages=messages), 422

    return app
