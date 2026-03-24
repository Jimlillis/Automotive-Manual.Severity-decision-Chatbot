// src/pages/LoginPage.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User as UserIcon } from 'lucide-react';

// Πώς μοιάζει ο χρήστης που έρχεται από τη βάση
interface DBUser {
  user_id: number;
  full_name: string;
  email: string;
}

const LoginPage: React.FC = () => {
  const [users, setUsers] = useState<DBUser[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Τραβάμε τους χρήστες από το FastAPI
    fetch('http://localhost:8000/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
      .catch(err => console.error("Σφάλμα φόρτωσης χρηστών:", err));
  }, []);

  const handleUserSelect = (userId: number) => {
    // Αποθηκεύουμε το ID του χρήστη στον browser
    localStorage.setItem('currentUserId', userId.toString());
    // Πάμε στο Dashboard
    navigate('/dashboard'); 
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0c0f12', color: 'white', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <h1 style={{ fontSize: '32px', marginBottom: '10px' }}>Επιλογή Προφίλ</h1>
      <p style={{ color: '#9ca3af', marginBottom: '40px' }}>Επιλέξτε χρήστη για να συνεχίσετε (Dev Mode)</p>

      <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
        {users.map(user => (
          <div 
            key={user.user_id}
            onClick={() => handleUserSelect(user.user_id)}
            style={{
              backgroundColor: '#1a1d24', padding: '30px', borderRadius: '20px', cursor: 'pointer',
              display: 'flex', flexDirection: 'column', alignItems: 'center', width: '250px',
              border: '1px solid rgba(255,255,255,0.05)', transition: 'transform 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
            onMouseOut={(e) => e.currentTarget.style.transform = 'translateY(0)'}
          >
            <div style={{ backgroundColor: '#21252d', padding: '20px', borderRadius: '50%', marginBottom: '15px' }}>
              <UserIcon size={40} color="#a3c4dc" />
            </div>
            <h2 style={{ margin: '0', fontSize: '20px' }}>{user.full_name}</h2>
            <p style={{ color: '#9ca3af', fontSize: '14px', marginTop: '5px' }}>{user.email}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LoginPage;