from flask_memo.app import app
from flask_memo import db as db_mod


def _client(tmp_path):
    db_path = tmp_path / "api.db"
    app.config["TESTING"] = True
    app.config["DB_PATH"] = db_path
    db_mod.init_db(db_path)
    return app.test_client()


def test_api_lifecycle(tmp_path):
    client = _client(tmp_path)

    # 追加
    resp = client.post(
        "/api/memos",
        json={"text": "hello"},
        follow_redirects=True,
    )
    assert resp.status_code == 201
    memo_id = resp.get_json()["id"]

    # 一覧取得
    resp = client.get("/api/memos")
    assert resp.status_code == 200
    data = resp.get_json()
    assert any(m["text"] == "hello" for m in data)

    # 削除
    resp = client.delete(f"/api/memos/{memo_id}")
    assert resp.status_code == 200
    assert resp.get_json() == {"ok": True}
