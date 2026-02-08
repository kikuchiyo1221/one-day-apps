import { useState, useEffect } from "react";

const API = "";

export default function TaskDetail({ task, members, onUpdate, onClose }) {
  const [comments, setComments] = useState([]);
  const [body, setBody] = useState("");
  const [memberId, setMemberId] = useState(members[0]?.id || "");

  useEffect(() => {
    fetchComments();
  }, [task.id]);

  useEffect(() => {
    if (members.length > 0 && !memberId) {
      setMemberId(members[0].id);
    }
  }, [members, memberId]);

  const fetchComments = async () => {
    const res = await fetch(`${API}/api/tasks/${task.id}/comments`);
    setComments(await res.json());
  };

  const addComment = async (e) => {
    e.preventDefault();
    if (!body.trim() || !memberId) return;
    await fetch(`${API}/api/tasks/${task.id}/comments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ member_id: memberId, body: body.trim() }),
    });
    setBody("");
    fetchComments();
  };

  return (
    <div style={styles.card}>
      <div style={styles.headerRow}>
        <h2 style={styles.title}>{task.title}</h2>
        <button onClick={onClose} style={styles.closeBtn}>
          ✕
        </button>
      </div>

      {task.description && <p style={styles.desc}>{task.description}</p>}

      <label style={styles.label}>Status</label>
      <select
        value={task.status}
        onChange={(e) => onUpdate(task.id, { status: e.target.value })}
        style={styles.select}
      >
        <option value="todo">To Do</option>
        <option value="in_progress">In Progress</option>
        <option value="done">Done</option>
      </select>

      <label style={styles.label}>Assignee</label>
      <select
        value={task.assignee_id || ""}
        onChange={(e) =>
          onUpdate(task.id, { assignee_id: Number(e.target.value) || null })
        }
        style={styles.select}
      >
        <option value="">Unassigned</option>
        {members.map((m) => (
          <option key={m.id} value={m.id}>
            {m.name}
          </option>
        ))}
      </select>

      <h3 style={styles.commentsTitle}>Comments ({comments.length})</h3>
      <ul style={styles.commentList}>
        {comments.map((c) => (
          <li key={c.id} style={styles.comment}>
            <strong>{c.member_name}</strong>
            <p style={styles.commentBody}>{c.body}</p>
            <span style={styles.commentDate}>{c.created_at}</span>
          </li>
        ))}
      </ul>

      {members.length > 0 && (
        <form onSubmit={addComment} style={styles.commentForm}>
          <select
            value={memberId}
            onChange={(e) => setMemberId(Number(e.target.value))}
            style={styles.select}
          >
            {members.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="Write a comment..."
            rows={2}
            style={styles.textarea}
          />
          <button type="submit" style={styles.sendBtn}>
            Send
          </button>
        </form>
      )}
    </div>
  );
}

const styles = {
  card: {
    background: "#f8f9fa",
    borderRadius: 8,
    padding: 16,
    border: "1px solid #dee2e6",
  },
  headerRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  },
  title: { fontSize: 18, margin: 0 },
  closeBtn: {
    background: "none",
    border: "none",
    fontSize: 18,
    cursor: "pointer",
  },
  desc: { color: "#495057", fontSize: 14, margin: "8px 0" },
  label: {
    display: "block",
    fontSize: 12,
    fontWeight: 600,
    color: "#6c757d",
    marginTop: 12,
    marginBottom: 4,
  },
  select: {
    width: "100%",
    padding: "6px 8px",
    borderRadius: 4,
    border: "1px solid #ced4da",
    fontSize: 14,
  },
  commentsTitle: { fontSize: 14, marginTop: 16, marginBottom: 8 },
  commentList: { listStyle: "none", padding: 0, margin: 0 },
  comment: {
    padding: "8px 0",
    borderBottom: "1px solid #e9ecef",
    fontSize: 13,
  },
  commentBody: { margin: "4px 0" },
  commentDate: { fontSize: 11, color: "#adb5bd" },
  commentForm: { marginTop: 12, display: "flex", flexDirection: "column", gap: 6 },
  textarea: {
    padding: "6px 8px",
    borderRadius: 4,
    border: "1px solid #ced4da",
    fontSize: 14,
    resize: "vertical",
  },
  sendBtn: {
    padding: "6px 12px",
    background: "#0d6efd",
    color: "#fff",
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
    fontSize: 14,
    alignSelf: "flex-end",
  },
};
