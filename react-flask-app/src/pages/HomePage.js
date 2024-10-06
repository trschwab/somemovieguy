import React from "react";
import { Link } from "react-router-dom";
import './styles_v2.css';
import styles from './styles';
import BasicExample from '../components/NavbarComponent';

const HomePage = () => {

  return (
    <div style={styles.container}>
        <BasicExample />

      {/* Main Content */}
      <div style={styles.contentContainer}>
        <div style={styles.contentBox}>
          <p style={styles.paragraph}>

            </p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
