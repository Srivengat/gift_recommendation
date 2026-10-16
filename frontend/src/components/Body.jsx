import gift from './gift.jpg';
import { useNavigate } from 'react-router-dom';
function Body() {
    const navigate = useNavigate();
    return(
        <section className="body">
            <div className="bol">
                <span className="one">
                    AI Powered Gifting 🎁
                </span>
                <h1 className= "two">The thought <br/> counts.
                    <br/>
                    <span>We help you find it.</span>
                </h1>
                <p>Find the perfect gift for your loved ones 🎁  
                    Our AI analyzes interests to recommend gifts they'll actually cherish
                </p>
                <button className="ct" onClick={() => navigate('/chat')}>Start Chat💬</button>
            </div>
            <div className="bor">
                <img src={gift} alt="giftimage" />
            </div>

        </section>
    )
}
export default Body ;