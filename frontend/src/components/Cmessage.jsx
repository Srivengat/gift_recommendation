import { useEffect, useRef } from "react";
import axios from "axios";

function Cmessage({ messages, recommendations, done, sessionId }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, recommendations]);

  const handleBuy = async (giftId) => {
    try {
      const res = await axios.post("http://localhost:8000/order/create", {
        session_id: sessionId,
        gift_id: giftId,
      });

      alert("Order created! Order ID: " + res.data.order_id);
    } catch (err) {
      console.error(err);
      alert("Failed to create order");
    }
  };

  return (
    <div className="cmsg">
      <div className="day">TODAY</div>

      {messages.map((m, i) => (
        <div key={i} className={`msg-row ${m.sender}`}>
          {m.sender === "bot" && <div className="bot-icon">🎁</div>}
          <div className="msg-bubble">{m.text}</div>
        </div>
      ))}

      {/* PRODUCT SECTION */}
      {done && recommendations.length > 0 && (
        <div className="product-section">
          {recommendations.map((r) => (
            <div key={r.gift_id} className="product-card">
              <img
                src={`http://localhost:8000${r.image_url}`}
                alt={r.name}
                className="product-img"
              /> 


              <div className="product-body">
                <h4>{r.name}</h4>
                <p className="price">₹{r.price}</p>

                <button
                  className="buy-btn"
                  onClick={() => handleBuy(r.gift_id)}
                >
                  Buy
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}

export default Cmessage;
