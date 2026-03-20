import React from 'react';
import { User, Phone } from 'lucide-react';
import styles from './UserCard.module.css';

const UserCard: React.FC = () => {
  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.avatar}>
          <User size={36} className={styles.avatarIcon} />
        </div>
        <div>
          <h2 className={styles.name}>Γιώργος Παπαδόπουλος</h2>
          <span className={styles.status}>Premium Member</span>
        </div>
      </div>

      <div className={styles.details}>
        <div className={styles.detailItem}>
          <Phone size={20} className={styles.detailIcon} />
          <span className={styles.label}>Τηλέφωνο:</span>
          <span className={styles.value}>+30 694... (Placeholder)</span>
        </div>
        {/* Θα προσθέσουμε κι άλλα στοιχεία αργότερα */}
      </div>
    </div>
  );
};

export default UserCard;