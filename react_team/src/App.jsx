import { useState, useEffect, useCallback } from "react";
import MemberList from "./MemberList.jsx";
import TaskBoard from "./TaskBoard.jsx";
import TaskDetail from "./TaskDetail.jsx";

const API = "";

export default function App() {
  const [members, setMembers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);

  const fetchMembers = useCallback(async () => {
    const res = await fetch(`${API}/api/members`);
    setMembers(await res.json());
  }, []);

  const fetchTasks = useCallback(async () => {
    const res = await fetch(`${API}/api/tasks`);
    setTasks(await res.json());
  }, []);

  useEffect(() => {
    fetchMembers();
    fetchTasks();
  }, [fetchMembers, fetchTasks]);

  const addMember = async (name, role) => {
    await fetch(`${API}/api/members`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, role }),
    });
    fetchMembers();
  };

  const deleteMember = async (id) => {
    await fetch(`${API}/api/members/${id}`, { method: "DELETE" });
    fetchMembers();
    fetchTasks();
  };

  const addTask = async (title, description, assigneeId) => {
    await fetch(`${API}/api/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description,
        assignee_id: assigneeId || null,
      }),
    });
    fetchTasks();
  };

  const updateTask = async (id, updates) => {
    const res = await fetch(`${API}/api/tasks/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
    const updated = await res.json();
    fetchTasks();
    if (selectedTask && selectedTask.id === id) {
      setSelectedTask(updated);
    }
  };

  const deleteTask = async (id) => {
    await fetch(`${API}/api/tasks/${id}`, { method: "DELETE" });
    fetchTasks();
    if (selectedTask && selectedTask.id === id) {
      setSelectedTask(null);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Team Collaboration Board</h1>
      <div style={styles.layout}>
        <aside style={styles.sidebar}>
          <MemberList
            members={members}
            onAdd={addMember}
            onDelete={deleteMember}
          />
        </aside>
        <main style={styles.main}>
          <TaskBoard
            tasks={tasks}
            members={members}
            onAdd={addTask}
            onUpdate={updateTask}
            onDelete={deleteTask}
            onSelect={setSelectedTask}
          />
        </main>
        {selectedTask && (
          <aside style={styles.detail}>
            <TaskDetail
              task={selectedTask}
              members={members}
              onUpdate={updateTask}
              onClose={() => setSelectedTask(null)}
            />
          </aside>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: "'Segoe UI', sans-serif",
    maxWidth: 1200,
    margin: "0 auto",
    padding: 16,
    color: "#1a1a2e",
  },
  header: {
    textAlign: "center",
    marginBottom: 24,
    fontSize: 28,
    fontWeight: 700,
  },
  layout: {
    display: "flex",
    gap: 16,
    alignItems: "flex-start",
  },
  sidebar: {
    width: 220,
    flexShrink: 0,
  },
  main: {
    flex: 1,
    minWidth: 0,
  },
  detail: {
    width: 300,
    flexShrink: 0,
  },
};
