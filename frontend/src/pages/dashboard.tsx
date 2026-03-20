// src/pages/Dashboard/Dashboard.tsx
import React from 'react';
import UserCard from '../../src/components/UserCard/UserCard';
import CarCard from '../../src/components/CarCard/CarCard';
import EmergencyButton from '../../src/components/Buttons/EmergencyButton';
import ManualButton from '../../src/components/Buttons/ManualButton';
import styles from './dashboard.module.css';

const Dashboard: React.FC = () => {
  return (
    <div className={styles.container}>
      {/* 1-2 απλά πράγματα στο Header */}
      <header className={styles.header}>
        <h1 className={styles.appTitle}>AutoAssist</h1>
        <p className={styles.appSubtitle}>Ο ψηφιακός σας βοηθός (Placeholder)</p>
      </header>

      {/* Main content grid */}
      <main className={styles.mainContent}>
        
        {/* Επάνω σειρά (Χρήστης & Αυτοκίνητο) */}
        <div className={styles.topRowGrid}>
          <div className={styles.gridItem}>
            <UserCard />
          </div>
          <div className={styles.gridItem}>
            <CarCard />
          </div>
        </div>

        {/* Κάτω σειρά (Κουμπιά) */}
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