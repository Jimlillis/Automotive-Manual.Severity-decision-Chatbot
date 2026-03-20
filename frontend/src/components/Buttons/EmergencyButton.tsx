import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { useNavigate } from 'react-router-dom'; // Εισαγωγή του hook
import styles from './Buttons.module.css';

const EmergencyButton: React.FC = () => {
  const navigate = useNavigate(); // Αρχικοποίηση

  const handleClick = () => {
    console.log('Emergency chatbot initiated');
    // Πλοήγηση στο path /chat
    navigate('../../pages/ChatPage.tsx'); 
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