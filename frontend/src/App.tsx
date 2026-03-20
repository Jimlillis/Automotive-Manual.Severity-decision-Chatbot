import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from '../src/pages/dashboard'; 
import ChatPage from '../src/pages/ChatPage'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  );
}

export default App;