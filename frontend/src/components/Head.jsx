function Head(){
    return(

        <nav className="navbar">
            <div className="logo">
                <span className="icon">🎁</span>
                <span className="text">AI Gift Assistant</span>
            </div>
            <ul className="info">
                <li>How it works</li>
                <li>Gift ideas</li>
                <li>About us</li>
            </ul>
            
            <div className="authn">
                <button className="login">Login</button>
                <button className="signup">Sign Up</button>
            </div>
        

         </nav>
    )
}
export default Head;