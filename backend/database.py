
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "examguard.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            photo_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            duration_minutes INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS exam_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'created',
            started_at TIMESTAMP,
            ended_at TIMESTAMP,
            FOREIGN KEY (candidate_id) REFERENCES candidates(id),
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        );
    """)
    connection.execute(
            """
            INSERT INTO exams (title, description, duration_minutes)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM exams WHERE title = ?
            )
            """,
            (
                "Sample Online Exam",
                "A sample exam for Sprint 2 testing",
                60,
                "Sample Online Exam",
            ),
        )

    connection.commit()
    connection.close()
if __name__ == "__main__":
    init_db()
    print("Database and tables created successfully!")