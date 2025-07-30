from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 簡易メモ保存（インメモリ）。本番では DB に置き換える予定
memos: list[str] = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("memo", "").strip()
        if text:
            memos.append(text)
        return redirect(url_for("index"))
    return render_template("index.html", memos=memos)


if __name__ == "__main__":
    app.run(debug=True) 