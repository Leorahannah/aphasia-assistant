import React, { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [role, setRole] = useState("non-aphasia");
  const [aphasiaSuggestions, setAphasiaSuggestions] = useState([]);

  const handleSend = async () => {
    if (!input.trim()) return;

    if (role === "non-aphasia") {
      const newMessage = {
        role: "non-aphasia",
        text: input.trim(),
      };
      setMessages((prev) => [...prev, newMessage]);
      setInput("");
    } else {
      // Send keywords + context to backend
      const context = messages
        .map((m) => `${m.role === "non-aphasia" ? "Them" : "You"}: ${m.text}`)
        .join("\n");

      try {
        const response = await fetch("http://127.0.0.1:5000/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            keywords: input.trim(),
            context: context,
          }),
        });

        const data = await response.json();
        setAphasiaSuggestions(data.completions || []);
      } catch (err) {
        console.error("Error generating suggestions:", err);
        setAphasiaSuggestions(["(Error fetching suggestions)"]);
      }
    }
  };

  const handlePickSuggestion = (suggestion) => {
    const newMessage = {
      role: "aphasia",
      text: suggestion,
    };
    setMessages((prev) => [...prev, newMessage]);
    setAphasiaSuggestions([]);
    setInput("");
  };

  return (
    <div className="App">
      <header>
        <h1>🧠 Leora's Aphasia Chat</h1>
        <div className="role-toggle">
          <label>Talking as: </label>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="non-aphasia">🩶 Non-Aphasia</option>
            <option value="aphasia">💙 Aphasia</option>
          </select>
        </div>
      </header>

      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role === "non-aphasia" ? "left grey" : "right blue"}`}
          >
            {msg.text}
          </div>
        ))}
        {aphasiaSuggestions.length > 0 && (
          <div className="suggestions">
            <p>Pick a sentence:</p>
            {aphasiaSuggestions.map((s, i) => (
              <button key={i} onClick={() => handlePickSuggestion(s)}>
                {s}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="input-bar">
        <input
          type="text"
          placeholder={role === "aphasia" ? "Type keywords..." : "Type full message..."}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
