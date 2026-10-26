
from flask import Blueprint, jsonify, request, session
from backend.database import get_db_connection

exam_bp = Blueprint("exam", __name__)


@exam_bp.route("/exams", methods=["GET"])
def get_exams():
    connection = get_db_connection()

    try:
        exams = connection.execute(
            """
            SELECT id, title, description, duration_minutes
            FROM exams
            ORDER BY id
            """
        ).fetchall()

        return jsonify({
            "exams": [dict(exam) for exam in exams]
        }), 200

    finally:
        connection.close()


@exam_bp.route("/sessions/start", methods=["POST"])
def start_session():
    candidate_id = session.get("candidate_id")

    if not candidate_id:
        return jsonify({
            "error": "Please log in before starting an exam"
        }), 401

    data = request.get_json(silent=True) or {}
    exam_id = data.get("exam_id")

    if not exam_id:
        return jsonify({
            "error": "Exam ID is required"
        }), 400

    connection = get_db_connection()

    try:
        exam = connection.execute(
            "SELECT id FROM exams WHERE id = ?",
            (exam_id,)
        ).fetchone()

        if not exam:
            return jsonify({
                "error": "Exam not found"
            }), 404

        cursor = connection.execute(
            """
            INSERT INTO exam_sessions (candidate_id, exam_id, status, started_at)
            VALUES (?, ?, 'in_progress', CURRENT_TIMESTAMP)
            """,
            (candidate_id, exam_id)
        )

        connection.commit()

        return jsonify({
            "message": "Exam session started successfully",
            "session_id": cursor.lastrowid,
            "candidate_id": candidate_id,
            "exam_id": exam_id,
            "status": "in_progress"
        }), 201

    finally:
        connection.close()
