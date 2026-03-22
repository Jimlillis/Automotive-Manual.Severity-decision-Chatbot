// src/components/UserCard/UserCard.tsx
import React from 'react';
import { User, Phone, ShieldCheck, FileText } from 'lucide-react';
import styles from './UserCard.module.css';

const UserCard: React.FC = () => {
  return (
    <div className={styles.card}>
      {/* Το Header είναι κεντραρισμένο */}
      <div className={styles.header}>
        <div className={styles.avatar}>
          <User size={32} className={styles.avatarIcon} />
        </div>
        <h2 className={styles.name}>Γιώργος Παπαδόπουλος</h2>
        <span className={styles.status}>PREMIUM MEMBER</span>
      </div>

      {/* Η λίστα είναι αριστερά στοιχισμένη */}
      <div className={styles.details}>
        <div className={styles.detailItem}>
          <div className={styles.iconContainer}>
            <Phone size={18} />
          </div>
          <div className={styles.textContainer}>
            <span className={styles.label}>Τηλέφωνο Επικοινωνίας</span>
            <span className={styles.value}>+30 210 123 4567</span>
          </div>
        </div>

        <div className={styles.detailItem}>
          <div className={styles.iconContainer}>
            <ShieldCheck size={18} />
          </div>
          <div className={styles.textContainer}>
            <span className={styles.label}>Ασφαλιστική Εταιρεία</span>
            <span className={styles.value}>Εθνική Ασφαλιστική</span>
          </div>
        </div>

        <div className={styles.detailItem}>
          <div className={styles.iconContainer}>
            <FileText size={18} />
          </div>
          <div className={styles.textContainer}>
            <span className={styles.label}>Αριθμός Συμβολαίου</span>
            <span className={styles.value}>POL-987654321</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserCard;