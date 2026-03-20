import React from 'react';
import { AlertTriangle } from 'lucide-react';
import styles from './Buttons.module.css';

const EmergencyButton: React.FC = () => {
  const handleClick = () => {
    console.log('Emergency chatbot initiated');
    // Εδώ θα μπει η λογική αργότερα
  };

  return (
    <button onClick={handleClick} className={`${styles.button} ${styles.emergency}`}>
      <div className={styles.iconContainer}>
        <AlertTriangle size={24} className={styles.icon} />
      </div>
      <div className={styles.textContainer}>
        <h3 className={styles.title}>Οδική Βοήθεια</h3>
        <p className={styles.subtitle}>Άμεση επικοινωνία σε περίπτωση ανάγκης</p>
      </div>
    </button>
  );
};

export default EmergencyButton;