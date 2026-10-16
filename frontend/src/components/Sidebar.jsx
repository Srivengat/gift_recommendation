function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidetop">
        <div className="licon">
          <span className="llogo">🎁</span>
          <span className="ltext">Gift Assistant</span>
        </div>

        <button className="but">＋ New Chat</button>

        <div >
            <input
              className="srch"
              placeholder="Search a conversation..."/>
        </div>

        <p className="rc1">RECENT CHATS</p>


      </div>
    </aside>
  );
}

export default Sidebar;
