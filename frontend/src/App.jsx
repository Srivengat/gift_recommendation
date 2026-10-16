import {BrowserRouter ,Routes,Route} from 'react-router-dom'

import Chat from './Chat.jsx';
import './App.css'
import Landing from './Landing.jsx';

function App() {

  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={< Landing/>} />
      <Route path="/chat" element={<Chat />} />
    </Routes>
    </BrowserRouter>

  )
}                                                   

export default App
