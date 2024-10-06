import React from "react";
import { Link } from "react-router-dom";
import './styles_v2.css';
import styles from './styles';
import BasicExample from '../components/NavbarComponent';

const AboutPage = () => {

  return (
    <div style={styles.container}>
        <BasicExample />

      {/* Main Content */}
      <div style={styles.contentContainer}>
        <div style={styles.contentBox}>
          <p style={styles.paragraph}>
              SomeMovieGuy
              <br></br><br></br>
              This is a basic implementation of a small project I've worked on, on and off, for a little while now. 
              I've slowly become a more and more active Letterboxd user over the past few years and an implementation of 
              reading their statistics and generating topsters for users was something I found to be a useful exercise in 
              my coding life, and something I found to be very interesting and fun. The website originally was just some 
              poorly organized code from Vim I had printing in the terminal, and slowly it transformed into raw HTML, then 
              Django, and now in it's final form as React and Flask code.
              <br></br><br></br>
              I really hope to keep working on this slowly and surely, making more efficient code, cleaner oriented designs,
              more user friendly experiences, and more features that movie lovers can use.
              <br></br><br></br>
              TODO
            </p>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
