import { useEffect, useState } from "react";
import Chead from "./Chead";
import Cmsg from "./Cmessage";
import Cinput from "./Cinput";
import { startChat, sendChatMessage } from "../api/Chatapi";

function Chatbar() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [done, setDone] = useState(false);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    const initChat = async () => {
      const res = await startChat();
      setSessionId(res.data.session_id);
      setMessages([{ sender: "bot", text: res.data.reply }]);
    };
    initChat();
  }, []);

  const handleSend = async (text) => {
    if (!sessionId) return;

    setMessages((p) => [...p, { sender: "user", text }]);

    const res = await sendChatMessage(sessionId, text);

    setMessages((p) => [...p, { sender: "bot", text: res.data.reply }]);
    setDone(res.data.done);

    if (res.data.recommendations) {
      setRecommendations(res.data.recommendations);
    }
  };



  return (
  <section className="chatlay">
    <Chead />
    <Cmsg
      messages={messages}
      recommendations={recommendations}
      done={done}
      sessionId={sessionId}
    />
    {!done && <Cinput onSend={handleSend} />}
  </section>
);

}

export default Chatbar;
