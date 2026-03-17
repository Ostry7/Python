import { useState, useEffect } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/messages")
      .then(res => res.json())
      .then(data => setMessages(data));
  }, []);

  const addMessage = async () => {
    const res = await fetch("http://localhost:5000/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const newMsg = await res.json();
    setMessages([...messages, newMsg]);
    setText("");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Minimalny MERN</h1>
      <input value={text} onChange={e => setText(e.target.value)} placeholder="Napisz wiadomość" />
      <button onClick={addMessage}>Dodaj</button>
      <ul>
        {messages.map(msg => <li key={msg._id}>{msg.text}</li>)}
      </ul>
    </div>
  );
}

export default App;
