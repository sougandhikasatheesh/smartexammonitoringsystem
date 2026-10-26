
import os
from flask import Flask, jsonify
from backend.database import init_db
from backend.routes.auth import auth_bp
from backend.routes.exam import exam_bp

def create_app():
    app = Flask(__name__)

    # Configure session security
    app.config["SECRET_KEY"] = os.environ.get(
        "EXAMGUARD_SECRET_KEY",
        "dev-secret-key-change-before-deployment"
    )
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    # Initialize database
    init_db()

    # Register authentication routes
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(exam_bp, url_prefix="/api/v1")

    @app.route("/")
    def home():
        return jsonify({
            "message": "ExamGuard Backend is running"
        })

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy"
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
