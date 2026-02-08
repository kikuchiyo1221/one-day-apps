import { useState } from "react";

export default function MemberList({ members, onAdd, onDelete }) {
  const [name, setName] = useState("");
  const [role, setRole] = useState("member");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    onAdd(name.trim(), role);
    setName("");
    setRole("member");
  };

  return (
    <div style={styles.card}>
      <h2 style={styles.title}>Members</h2>
      <ul style={styles.list}>
        {members.map((m) => (
          <li key={m.id} style={styles.item}>
            <div>
              <strong>{m.name}</strong>
              <span style={styles.role}>{m.role}</span>
            </div>
            <button onClick={() => onDelete(m.id)} style={styles.deleteBtn}>
              ✕
            </button>
          </li>
        ))}
      </ul>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          style={styles.input}
        />
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          style={styles.select}
        >
          <option value="member">Member</option>
          <option value="leader">Leader</option>
        </select>
        <button type="submit" style={styles.addBtn}>
          Add
        </button>
      </form>
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
  title: { fontSize: 18, margin: "0 0 12px" },
  list: { listStyle: "none", padding: 0, margin: "0 0 12px" },
  item: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "6px 0",
    borderBottom: "1px solid #e9ecef",
  },
  role: {
    display: "block",
    fontSize: 12,
    color: "#6c757d",
  },
  deleteBtn: {
    background: "none",
    border: "none",
    color: "#dc3545",
    cursor: "pointer",
    fontSize: 14,
  },
  form: { display: "flex", flexDirection: "column", gap: 6 },
  input: {
    padding: "6px 8px",
    borderRadius: 4,
    border: "1px solid #ced4da",
    fontSize: 14,
  },
  select: {
    padding: "6px 8px",
    borderRadius: 4,
    border: "1px solid #ced4da",
    fontSize: 14,
  },
  addBtn: {
    padding: "6px 12px",
    background: "#0d6efd",
    color: "#fff",
    border: "none",
    borderRadius: 4,
    cursor: "pointer",
    fontSize: 14,
  },
};
