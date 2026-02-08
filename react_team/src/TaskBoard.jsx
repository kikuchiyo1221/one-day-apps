import { useState } from "react";

const COLUMNS = [
  { key: "todo", label: "To Do", color: "#e9ecef" },
  { key: "in_progress", label: "In Progress", color: "#fff3cd" },
  { key: "done", label: "Done", color: "#d1e7dd" },
];

export default function TaskBoard({
  tasks,
  members,
  onAdd,
  onUpdate,
  onDelete,
  onSelect,
}) {
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [assignee, setAssignee] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    onAdd(title.trim(), desc.trim(), assignee || null);
    setTitle("");
    setDesc("");
    setAssignee("");
  };

  const handleDragStart = (e, taskId) => {
    e.dataTransfer.setData("text/plain", taskId);
  };

  const handleDrop = (e, status) => {
    e.preventDefault();
    const taskId = Number(e.dataTransfer.getData("text/plain"));
    onUpdate(taskId, { status });
  };

  return (
    <div>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          style={styles.input}
        />
        <input
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
          placeholder="Description"
          style={styles.input}
        />
        <select
          value={assignee}
          onChange={(e) => setAssignee(e.target.value)}
          style={styles.select}
        >
          <option value="">Unassigned</option>
          {members.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </select>
        <button type="submit" style={styles.addBtn}>
          Add Task
        </button>
      </form>

      <div style={styles.board}>
        {COLUMNS.map((col) => (
          <div
            key={col.key}
            style={{ ...styles.column, background: col.color }}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => handleDrop(e, col.key)}
          >
            <h3 style={styles.colTitle}>
              {col.label} (
              {tasks.filter((t) => t.status === col.key).length})
            </h3>
            {tasks
              .filter((t) => t.status === col.key)
              .map((task) => (
                <div
                  key={task.id}
                  draggable
                  onDragStart={(e) => handleDragStart(e, task.id)}
                  style={styles.card}
                  onClick={() => onSelect(task)}
                >
                  <div style={styles.cardTitle}>{task.title}</div>
                  {task.assignee_name && (
                    <div style={styles.assignee}>{task.assignee_name}</div>
                  )}
                  <div style={styles.actions}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDelete(task.id);
                      }}
                      style={styles.deleteBtn}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  form: {
    display: "flex",
    gap: 8,
    marginBottom: 16,
    flexWrap: "wrap",
  },
  input: {
    padding: "8px 10px",
    borderRadius: 4,
    border: "1px solid #ced4da",
    fontSize: 14,
    flex: "1 1 150px",
  },
  select: {
    padding: "8px 10px",
    borderRadius: 4,
    border: "1px solid #ced4da",
    fontSize: 14,
  },
  addBtn: {
    padding: "8px 16px",
    background: "#198754",
    color: "#fff",
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
    fontSize: 14,
  },
  board: {
    display: "flex",
    gap: 12,
  },
  column: {
    flex: 1,
    borderRadius: 8,
    padding: 12,
    minHeight: 200,
  },
  colTitle: {
    fontSize: 16,
    margin: "0 0 12px",
  },
  card: {
    background: "#fff",
    borderRadius: 6,
    padding: 10,
    marginBottom: 8,
    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    cursor: "grab",
  },
  cardTitle: {
    fontWeight: 600,
    marginBottom: 4,
  },
  assignee: {
    fontSize: 12,
    color: "#6c757d",
    marginBottom: 4,
  },
  actions: {
    display: "flex",
    justifyContent: "flex-end",
  },
  deleteBtn: {
    background: "none",
    border: "none",
    color: "#dc3545",
    cursor: "pointer",
    fontSize: 12,
  },
};
