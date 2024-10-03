import React from "react";
import { Link } from "react-router-dom";
import './styles_v2.css';
import styles from './styles';

const HomePage = () => {

  return (
    <div style={styles.container}>
      {/* Navigation Header */}
      <header style={styles.header}>
        {/* <Link to="/" style={styles.logo}>SomeMovieGuy</Link> */}
        <nav>
          <ul style={styles.navLinks}>
            <li>
              <Link to="/" style={styles.navLink}>Home</Link>
            </li>
            <li>
              <Link to="/about" style={styles.navLink}>About</Link>
            </li>
          </ul>
        </nav>
      </header>

      {/* Main Content */}
      <div style={styles.contentContainer}>
        <div style={styles.contentBox}>
          {/* <h3 style={styles.heading}>Hi, I’m Troy and this is my website.</h3> */}
          <p style={styles.paragraph}>
              Some Movie Guy
              <br></br><br></br>
              About
              <br></br><br></br>
              More info
              <br></br><br></br>
              Here
            </p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
