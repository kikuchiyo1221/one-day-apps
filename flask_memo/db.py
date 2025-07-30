import sqlite3
from pathlib import Path
from typing import List, Dict, Any

DEFAULT_DB_PATH = Path(__file__).with_suffix(".db")


def get_conn(db_path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path else DEFAULT_DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path | str | None = None) -> None:
    conn = get_conn(db_path)
    with conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL
        )"""
        )
    conn.close()


def add_memo(text: str, db_path: Path | str | None = None) -> int:
    conn = get_conn(db_path)
    with conn:
        cur = conn.execute("INSERT INTO memos(text) VALUES (?)", (text,))
        memo_id = cur.lastrowid
    conn.close()
    return memo_id


def get_memos(db_path: Path | str | None = None) -> List[Dict[str, Any]]:
    conn = get_conn(db_path)
    memos = [dict(row) for row in conn.execute("SELECT id, text FROM memos ORDER BY id DESC")] 
    conn.close()
    return memos


def delete_memo(memo_id: int, db_path: Path | str | None = None) -> None:
    conn = get_conn(db_path)
    with conn:
        conn.execute("DELETE FROM memos WHERE id=?", (memo_id,))
    conn.close() 