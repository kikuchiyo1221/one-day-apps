from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, current_app, jsonify
def _db_path():
    """設定で DB_PATH が指定されていればそのパスを返す。無ければ None。"""
    return current_app.config.get("DB_PATH")
from flask_cors import CORS
from . import db as db_mod

app = Flask(__name__)
CORS(app)

# DB 初期化（アプリコンテキスト内で行い、テスト時はカスタムパスを利用）
with app.app_context():
    db_mod.init_db(_db_path())


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("memo", "").strip()
        if text:
            # ❶ メモを DB に追加（現在の DB パスを渡す）
            db_mod.add_memo(text, _db_path())
        # 追加後は GET / へリダイレクト
        return redirect(url_for("index"))

    # ❷ DB からメモ一覧を取得してテンプレートへ
    memos = db_mod.get_memos(_db_path())
    return render_template("index.html", memos=memos)

@app.route("/delete/<int:memo_id>")
def delete(memo_id: int):
    db_mod.delete_memo(memo_id, _db_path())
    return redirect(url_for("index"))


@app.route("/api/memos", methods=["GET"])

def api_list():
    return jsonify(db_mod.get_memos(_db_path()))


@app.route("/api/memos", methods=["POST"])

def api_add():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return {"error": "text required"}, 400
    memo_id = db_mod.add_memo(text, _db_path())
    return {"id": memo_id, "text": text}, 201


@app.route("/api/memos/<int:memo_id>", methods=["DELETE"])

def api_delete(memo_id: int):
    db_mod.delete_memo(memo_id, _db_path())
    return {"ok": True}


if __name__ == "__main__":
    app.run(debug=True) 