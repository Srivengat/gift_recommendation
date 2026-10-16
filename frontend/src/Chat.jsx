import Sidebar from "./components/Sidebar";
import Chatbar from "./components/Chatbar";

function Chat() {
  return (
    <div className="cont">
      <Sidebar />
      <div className="divider"></div>
      <Chatbar />
    </div>
  );
}

export default Chat;
