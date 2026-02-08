from flask import Flask, request, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

db.init_db()

VALID_STATUSES = ("todo", "in_progress", "done")


# --- Members API ---

@app.route("/api/members", methods=["GET"])
def list_members():
    return jsonify(db.get_members())


@app.route("/api/members", methods=["POST"])
def create_member():
    data = request.get_json(force=True)
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    role = data.get("role", "member").strip()
    member = db.add_member(name, role)
    return jsonify(member), 201


@app.route("/api/members/<int:member_id>", methods=["DELETE"])
def remove_member(member_id):
    db.delete_member(member_id)
    return "", 204


# --- Tasks API ---

@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    return jsonify(db.get_tasks())


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    description = data.get("description", "")
    status = data.get("status", "todo")
    if status not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400
    assignee_id = data.get("assignee_id")
    task = db.add_task(title, description, status, assignee_id)
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def modify_task(task_id):
    data = request.get_json(force=True)
    status = data.get("status")
    if status is not None and status not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {VALID_STATUSES}"}), 400
    task = db.update_task(
        task_id,
        title=data.get("title"),
        description=data.get("description"),
        status=status,
        assignee_id=data.get("assignee_id"),
    )
    if task is None:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def remove_task(task_id):
    db.delete_task(task_id)
    return "", 204


# --- Comments API ---

@app.route("/api/tasks/<int:task_id>/comments", methods=["GET"])
def list_comments(task_id):
    return jsonify(db.get_comments(task_id))


@app.route("/api/tasks/<int:task_id>/comments", methods=["POST"])
def create_comment(task_id):
    data = request.get_json(force=True)
    member_id = data.get("member_id")
    body = data.get("body", "").strip()
    if not member_id:
        return jsonify({"error": "member_id is required"}), 400
    if not body:
        return jsonify({"error": "body is required"}), 400
    comment = db.add_comment(task_id, member_id, body)
    return jsonify(comment), 201


if __name__ == "__main__":
    app.run(debug=True, port=5001)
