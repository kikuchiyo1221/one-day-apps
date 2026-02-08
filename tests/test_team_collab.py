import sys
import os
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "team_collab"))
import db
from app import app


@pytest.fixture
def tmp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db.init_db(path)
    yield path
    os.unlink(path)


@pytest.fixture
def client(tmp_db, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_db)
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# --- Member tests ---

class TestMembers:
    def test_list_empty(self, client):
        res = client.get("/api/members")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_add_member(self, client):
        res = client.post("/api/members", json={"name": "Alice", "role": "leader"})
        assert res.status_code == 201
        data = res.get_json()
        assert data["name"] == "Alice"
        assert data["role"] == "leader"
        assert "id" in data

    def test_add_member_default_role(self, client):
        res = client.post("/api/members", json={"name": "Bob"})
        assert res.status_code == 201
        assert res.get_json()["role"] == "member"

    def test_add_member_empty_name(self, client):
        res = client.post("/api/members", json={"name": ""})
        assert res.status_code == 400

    def test_delete_member(self, client):
        res = client.post("/api/members", json={"name": "Alice"})
        member_id = res.get_json()["id"]
        res = client.delete(f"/api/members/{member_id}")
        assert res.status_code == 204
        res = client.get("/api/members")
        assert len(res.get_json()) == 0


# --- Task tests ---

class TestTasks:
    def test_list_empty(self, client):
        res = client.get("/api/tasks")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_add_task(self, client):
        res = client.post("/api/tasks", json={"title": "Setup CI"})
        assert res.status_code == 201
        data = res.get_json()
        assert data["title"] == "Setup CI"
        assert data["status"] == "todo"
        assert data["assignee_name"] is None

    def test_add_task_with_assignee(self, client):
        m = client.post("/api/members", json={"name": "Alice"}).get_json()
        res = client.post(
            "/api/tasks",
            json={"title": "Write docs", "assignee_id": m["id"]},
        )
        assert res.status_code == 201
        assert res.get_json()["assignee_name"] == "Alice"

    def test_add_task_empty_title(self, client):
        res = client.post("/api/tasks", json={"title": ""})
        assert res.status_code == 400

    def test_add_task_invalid_status(self, client):
        res = client.post("/api/tasks", json={"title": "X", "status": "bad"})
        assert res.status_code == 400

    def test_update_task_status(self, client):
        t = client.post("/api/tasks", json={"title": "Task"}).get_json()
        res = client.patch(f"/api/tasks/{t['id']}", json={"status": "in_progress"})
        assert res.status_code == 200
        assert res.get_json()["status"] == "in_progress"

    def test_update_task_not_found(self, client):
        res = client.patch("/api/tasks/999", json={"status": "done"})
        assert res.status_code == 404

    def test_delete_task(self, client):
        t = client.post("/api/tasks", json={"title": "Task"}).get_json()
        res = client.delete(f"/api/tasks/{t['id']}")
        assert res.status_code == 204
        assert len(client.get("/api/tasks").get_json()) == 0


# --- Comment tests ---

class TestComments:
    def test_add_and_list_comments(self, client):
        m = client.post("/api/members", json={"name": "Alice"}).get_json()
        t = client.post("/api/tasks", json={"title": "Task"}).get_json()
        res = client.post(
            f"/api/tasks/{t['id']}/comments",
            json={"member_id": m["id"], "body": "Looks good"},
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["body"] == "Looks good"
        assert data["member_name"] == "Alice"

        comments = client.get(f"/api/tasks/{t['id']}/comments").get_json()
        assert len(comments) == 1

    def test_add_comment_missing_body(self, client):
        m = client.post("/api/members", json={"name": "Alice"}).get_json()
        t = client.post("/api/tasks", json={"title": "Task"}).get_json()
        res = client.post(
            f"/api/tasks/{t['id']}/comments",
            json={"member_id": m["id"], "body": ""},
        )
        assert res.status_code == 400

    def test_add_comment_missing_member(self, client):
        t = client.post("/api/tasks", json={"title": "Task"}).get_json()
        res = client.post(
            f"/api/tasks/{t['id']}/comments",
            json={"body": "Hello"},
        )
        assert res.status_code == 400
