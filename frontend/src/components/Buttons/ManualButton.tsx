import React from 'react';
import { BookOpen } from 'lucide-react';
import styles from './Buttons.module.css';

const ManualButton: React.FC = () => {
  const handleClick = () => {
    console.log('Manual chatbot initiated');
  };

  return (
    <button onClick={handleClick} className={`${styles.button} ${styles.manual}`}>
      <div className={styles.iconContainer}>
        <BookOpen size={24} className={styles.icon} />
      </div>
      <div className={styles.textContainer}>
        <h3 className={styles.title}>Βοηθός Manual</h3>
        <p className={styles.subtitle}>Ρωτήστε οτιδήποτε για το όχημά σας</p>
      </div>
    </button>
  );
};

export default ManualButton;