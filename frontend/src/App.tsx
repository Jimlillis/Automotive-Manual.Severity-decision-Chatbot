import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from '../src/pages/dashboard'; 
import EmergencyChat from './pages/EmergencyChat/EmergencyChat'; 
import LoginPage from './pages/LoginPage/LoginPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard" element={<HomePage />} />
        <Route path="/chat" element={<EmergencyChat />} />
      </Routes>
    </Router>
  );
}

export default App;