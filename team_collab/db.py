import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "team.db")


def get_connection(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=None):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'member',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'todo',
            assignee_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assignee_id) REFERENCES members(id) ON DELETE SET NULL
        );
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            body TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


# --- Members ---

def get_members(db_path=None):
    conn = get_connection(db_path)
    rows = conn.execute("SELECT * FROM members ORDER BY created_at").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_member(name, role="member", db_path=None):
    conn = get_connection(db_path)
    cur = conn.execute(
        "INSERT INTO members (name, role) VALUES (?, ?)", (name, role)
    )
    conn.commit()
    member_id = cur.lastrowid
    row = conn.execute("SELECT * FROM members WHERE id = ?", (member_id,)).fetchone()
    conn.close()
    return dict(row)


def delete_member(member_id, db_path=None):
    conn = get_connection(db_path)
    conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()


# --- Tasks ---

def get_tasks(db_path=None):
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT t.*, m.name AS assignee_name
        FROM tasks t
        LEFT JOIN members m ON t.assignee_id = m.id
        ORDER BY t.created_at
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_task(title, description="", status="todo", assignee_id=None, db_path=None):
    conn = get_connection(db_path)
    cur = conn.execute(
        "INSERT INTO tasks (title, description, status, assignee_id) VALUES (?, ?, ?, ?)",
        (title, description, status, assignee_id),
    )
    conn.commit()
    task_id = cur.lastrowid
    row = conn.execute("""
        SELECT t.*, m.name AS assignee_name
        FROM tasks t LEFT JOIN members m ON t.assignee_id = m.id
        WHERE t.id = ?
    """, (task_id,)).fetchone()
    conn.close()
    return dict(row)


def update_task(task_id, title=None, description=None, status=None, assignee_id=None, db_path=None):
    conn = get_connection(db_path)
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        conn.close()
        return None
    t = dict(task)
    new_title = title if title is not None else t["title"]
    new_desc = description if description is not None else t["description"]
    new_status = status if status is not None else t["status"]
    new_assignee = assignee_id if assignee_id is not None else t["assignee_id"]
    conn.execute(
        "UPDATE tasks SET title=?, description=?, status=?, assignee_id=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (new_title, new_desc, new_status, new_assignee, task_id),
    )
    conn.commit()
    row = conn.execute("""
        SELECT t.*, m.name AS assignee_name
        FROM tasks t LEFT JOIN members m ON t.assignee_id = m.id
        WHERE t.id = ?
    """, (task_id,)).fetchone()
    conn.close()
    return dict(row)


def delete_task(task_id, db_path=None):
    conn = get_connection(db_path)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


# --- Comments ---

def get_comments(task_id, db_path=None):
    conn = get_connection(db_path)
    rows = conn.execute("""
        SELECT c.*, m.name AS member_name
        FROM comments c
        JOIN members m ON c.member_id = m.id
        WHERE c.task_id = ?
        ORDER BY c.created_at
    """, (task_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_comment(task_id, member_id, body, db_path=None):
    conn = get_connection(db_path)
    cur = conn.execute(
        "INSERT INTO comments (task_id, member_id, body) VALUES (?, ?, ?)",
        (task_id, member_id, body),
    )
    conn.commit()
    comment_id = cur.lastrowid
    row = conn.execute("""
        SELECT c.*, m.name AS member_name
        FROM comments c JOIN members m ON c.member_id = m.id
        WHERE c.id = ?
    """, (comment_id,)).fetchone()
    conn.close()
    return dict(row)
