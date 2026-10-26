
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from backend.database import get_db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    connection = get_db_connection()

    try:
        existing = connection.execute(
            "SELECT id FROM candidates WHERE email = ?",
            (email,)
        ).fetchone()

        if existing:
            return jsonify({
                "error": "Email is already registered"
            }), 409

        password_hash = generate_password_hash(password)

        cursor = connection.execute(
            """
            INSERT INTO candidates (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash)
        )

        connection.commit()

        return jsonify({
            "message": "Candidate registered successfully",
            "candidate_id": cursor.lastrowid
        }), 201

    finally:
        connection.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    connection = get_db_connection()

    try:
        candidate = connection.execute(
            """
            SELECT id, name, email, password_hash
            FROM candidates
            WHERE email = ?
            """,
            (email,)
        ).fetchone()
    finally:
        connection.close()

    if not candidate or not check_password_hash(
        candidate["password_hash"], password
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    session.clear()
    session["candidate_id"] = candidate["id"]

    return jsonify({
        "message": "Login successful",
        "candidate": {
            "id": candidate["id"],
            "name": candidate["name"],
            "email": candidate["email"]
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "message": "Logout successful"
    }), 200
