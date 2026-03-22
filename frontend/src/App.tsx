import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from '../src/pages/dashboard'; 
import EmergencyChat from './pages/EmergencyChat/EmergencyChat'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<EmergencyChat />} />
      </Routes>
    </Router>
  );
}

export default App;