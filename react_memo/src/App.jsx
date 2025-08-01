import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5000/api/memos";

export default function App() {
  const [memos, setMemos] = useState([]);
  const [text, setText] = useState("");

  // 一覧取得
  const load = async () => {
    const res = await fetch(API);
    const data = await res.json();
    setMemos(data);
  };

  // 初回だけ実行
  useEffect(() => {
    load();
  }, []);

  // 追加
  const addMemo = async () => {
    if (!text.trim()) return;
    await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    setText("");
    load();
  };

  // 削除
  const delMemo = async (id) => {
    await fetch(`${API}/${id}`, { method: "DELETE" });
    load();
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Memo App (React)</h1>
      <div>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="メモを入力"
          style={{ width: "70%" }}
        />
        <button onClick={addMemo}>追加</button>
      </div>
      <ul>
        {memos.map((m) => (
          <li key={m.id}>
            {m.text}{" "}
            <button onClick={() => delMemo(m.id)} style={{ marginLeft: 8 }}>
              削除
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}