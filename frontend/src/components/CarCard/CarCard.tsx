import React from 'react';
import styles from './CarCard.module.css';
import CarImage from '../../assets/car-placeholder.jpg';

const CarCard: React.FC = () => {
  return (
    <div className={styles.card}>
      <h2 className={styles.title}>Το Όχημά μου</h2>
      
      <div className={styles.imageContainer}>
        <img src={CarImage} alt="BMW Placeholder" className={styles.carImage} />
      </div>

      <div className={styles.simpleStats}>
        <div className={styles.stat}>
          <div className={styles.statLabel}>Μοντέλο:</div>
          <div className={styles.statValue}>BMW (Placeholder)</div>
        </div>
        <div className={styles.stat}>
          <div className={styles.statLabel}>Πινακίδα:</div>
          <div className={styles.statValue}>ΑΒΓ-1234 (Placeholder)</div>
        </div>
      </div>
    </div>
  );
};

export default CarCard;