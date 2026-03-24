import React from 'react';
import { Gauge, KeyRound, Wrench } from 'lucide-react'; // Προσθέσαμε το Wrench
import styles from './CarCard.module.css';
import CarImage from '../../assets/car-placeholder.jpg'; // Import της εικόνας

interface CarCardProps {
  car: {
    brand: string;
    model: string;
    licence_plate: string;
  };
}

const CarCard: React.FC<CarCardProps> = ({ car }) => {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.titleArea}>
          <h2 className={styles.title}>Το Όχημά μου</h2>
          <p className={styles.subtitle}>{car.brand} · {car.model}</p>
        </div>
      </div>
      
      {/* Container για την εικόνα με το spotlight effect */}
      <div className={styles.imageContainer}>
        <img src={CarImage} alt="BMW" className={styles.carImage} />
      </div>

      {/* Τα νέα στατιστικά στο κάτω μέρος */}
      <div className={styles.footerStats}>
        <div className={styles.statBadge}>
          <Gauge size={20} className={styles.statIcon} />
          <div className={styles.statText}>
            <span className={styles.statLabel}>ΧΙΛΙΟΜΕΤΡΑ</span>
            <span className={styles.statValue}>34,520 km</span>
          </div>
        </div>

        <div className={styles.statBadge}>
          <KeyRound size={20} className={styles.statIcon} />
          <div className={styles.statText}>
            <span className={styles.statLabel}>ΠΙΝΑΚΙΔΑ</span>
            <span className={styles.statValue}>{car.licence_plate}</span>
          </div>
        </div>

        <div className={styles.statBadge}>
          <Wrench size={20} className={styles.statIcon} />
          <div className={styles.statText}>
            <span className={styles.statLabel}>ΕΠΟΜΕΝΟ SERVICE</span>
            <span className={styles.statValue}>15/04/26</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CarCard;