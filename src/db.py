import hashlib
import hmac
import secrets
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

import constants

PASSWORD_HASH_PREFIX = "pbkdf2_sha256"
PASSWORD_SALT_BYTES = 16
PASSWORD_ITERATIONS = 120_000


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(constants.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    constants.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                filename TEXT NOT NULL,
                accuracy REAL NOT NULL,
                score REAL NOT NULL,
                correct_count INTEGER NOT NULL,
                total_count INTEGER NOT NULL,
                submitted_at TEXT NOT NULL,
                FOREIGN KEY(team_id) REFERENCES teams(id)
            )
            """
        )
        conn.commit()


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(PASSWORD_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return f"{PASSWORD_HASH_PREFIX}${salt.hex()}${digest.hex()}"


def _verify_password(stored_password: str, provided_password: str) -> bool:
    if not stored_password.startswith(f"{PASSWORD_HASH_PREFIX}$"):
        return hmac.compare_digest(stored_password, provided_password)

    try:
        _, salt_hex, digest_hex = stored_password.split("$", 2)
    except ValueError:
        return False

    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(digest_hex)
    computed = hashlib.pbkdf2_hmac(
        "sha256",
        provided_password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS,
    )
    return hmac.compare_digest(expected, computed)


def register_team(username: str, password: str) -> int:
    hashed_password = _hash_password(password.strip())
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO teams (username, password, created_at) VALUES (?, ?, ?)",
            (username.strip(), hashed_password, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cursor.lastrowid


def authenticate_team(username: str, password: str) -> Optional[Dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, password FROM teams WHERE username = ?",
            (username.strip(),),
        ).fetchone()

        if not row:
            return None

        stored_password = row["password"]
        if not _verify_password(stored_password, password):
            return None

        if not stored_password.startswith(f"{PASSWORD_HASH_PREFIX}$"):
            conn.execute(
                "UPDATE teams SET password = ? WHERE id = ?",
                (_hash_password(password.strip()), row["id"]),
            )
            conn.commit()

        return {"id": row["id"], "username": row["username"]}


def get_team_by_username(username: str) -> Optional[Dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username FROM teams WHERE username = ?",
            (username.strip(),),
        ).fetchone()
        return dict(row) if row else None


def save_submission(
    team_id: int,
    task: str,
    filename: str,
    accuracy: float,
    score: float,
    correct_count: int,
    total_count: int,
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO submissions (team_id, task, filename, accuracy, score, correct_count, total_count, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                team_id,
                task,
                filename,
                accuracy,
                score,
                correct_count,
                total_count,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_leaderboard(task: Optional[str] = None, limit: int = 50) -> List[Dict]:
    query = """
        SELECT
            t.username AS team,
            s.task,
            MAX(s.score) AS best_score,
            MAX(s.accuracy) AS best_accuracy,
            COUNT(*) AS attempts,
            MAX(s.submitted_at) AS last_submission
        FROM submissions s
        JOIN teams t ON s.team_id = t.id
    """
    params = []
    if task:
        query += " WHERE s.task = ?"
        params.append(task)
    query += " GROUP BY t.id, s.task ORDER BY best_score DESC, best_accuracy DESC, last_submission ASC LIMIT ?"
    params.append(limit)
    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def get_submission_history(team_id: int) -> List[Dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT task, filename, accuracy, score, correct_count, total_count, submitted_at FROM submissions WHERE team_id = ? ORDER BY submitted_at DESC",
            (team_id,),
        ).fetchall()
        return [dict(row) for row in rows]
