import { useState } from "react";

function Cinput({ onSend }) {
  const [input, setInput] = useState("");

  const send = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="chat-input-wrapper">
      <input
        className="chat-input"
        placeholder="Type a message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && send()}
      />
      <button className="send-btn" onClick={send}>↑</button>
    </div>
  );
}

export default Cinput;
