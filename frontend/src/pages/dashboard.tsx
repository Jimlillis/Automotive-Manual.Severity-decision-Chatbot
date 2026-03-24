// src/pages/Dashboard/Dashboard.tsx
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UserCard from '../../src/components/UserCard/UserCard';
import CarCard from '../../src/components/CarCard/CarCard';
import EmergencyButton from '../../src/components/Buttons/EmergencyButton';
import ManualButton from '../../src/components/Buttons/ManualButton';
import type { User, Car } from '../../src/types';
import styles from './Dashboard.module.css';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState<User | null>(null);
  const [carData, setCarData] = useState<Car | null>(null);

  useEffect(() => {
    const userId = localStorage.getItem('currentUserId');
    
    // Αν δεν υπάρχει επιλεγμένος χρήστης, τον στέλνουμε πίσω στο login
    if (!userId) {
      navigate('/');
      return;
    }

    // Ζητάμε τα δεδομένα από το FastAPI
    fetch(`http://localhost:8000/api/dashboard-data/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUserData(data.user);
        // Για απλότητα, παίρνουμε το πρώτο αυτοκίνητο του χρήστη αν έχει πολλά
        if (data.cars && data.cars.length > 0) {
          setCarData(data.cars[0]);
        }
      })
      .catch(err => console.error("Σφάλμα:", err));
  }, [navigate]);

  if (!userData) {
    return <div style={{ color: 'white', padding: '50px', textAlign: 'center' }}>Φόρτωση δεδομένων...</div>;
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 className={styles.appTitle}>AutoAssist</h1>
            <p className={styles.appSubtitle}>Ο ψηφιακός σας βοηθός</p>
          </div>
          {/* Κουμπί για Αποσύνδεση */}
          <button 
            onClick={() => { localStorage.removeItem('currentUserId'); navigate('/login'); }}
            style={{ backgroundColor: '#1e3a8a', color: 'white', padding: '8px 16px', borderRadius: '10px', border: 'none', cursor: 'pointer' }}
          >
            Αλλαγή Χρήστη
          </button>
        </div>
      </header>

      <main className={styles.mainContent}>
        <div className={styles.topRowGrid}>
          <div className={styles.gridItem}>
            {/* Περνάμε τα δεδομένα στο UserCard (Θα πρέπει να το τροποποιήσεις για να τα δέχεται ως props) */}
            <UserCard user={userData} />
          </div>
          <div className={styles.gridItem}>
            {/* Περνάμε τα δεδομένα στο CarCard */}
            {carData ? <CarCard car={carData} /> : <div style={{color: 'white'}}>Δεν βρέθηκε όχημα.</div>}
          </div>
        </div>

        <div className={styles.bottomRowGrid}>
          <div className={styles.gridItem}>
            <EmergencyButton />
          </div>
          <div className={styles.gridItem}>
            <ManualButton />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;