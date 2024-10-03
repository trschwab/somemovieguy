import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css'; // Importing the CSS file
import { Link } from "react-router-dom";
import './styles_v2.css';
import styles from './styles';

const HomePage = () => {
  const [username, setUsername] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [userData, setUserData] = useState([]);
  const [statsString, setStatsString] = useState('');
  const [topsterImageUrl, setTopsterImageUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStatsMessage, setLoadingStatsMessage] = useState('');
  const [loadingTopsterMessage, setLoadingTopsterMessage] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Clear previously displayed stats and topster
    setStatsString('');
    setTopsterImageUrl('');
    setValidationMessage('This might take a few minutes...');
    setLoadingStatsMessage('');
    setLoadingTopsterMessage('');
    setIsLoading(true);
  
    try {
      const userResponse = await fetch('/api/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
      });

      if (!userResponse.ok) {
        throw new Error('Oops, sorry about that, there was an internal error.');
      }

      const userData = await userResponse.json();
      console.log(userData);
      setUserData(userData.user_data);
      setValidationMessage(userData.message);
      
      // Set the loading message for stats
      setLoadingStatsMessage('Loading stats...');

      const statsResponse = await fetch(`/api/user_stats_string/${username}/`);

      if (!statsResponse.ok) {
        throw new Error('Oops, sorry about that, there was an internal error.');
      }

      const statsData = await statsResponse.json();
      console.log('Stats String Data:', statsData);
      setStatsString(JSON.stringify(statsData.return_string, null, 2));
      setLoadingStatsMessage('');
      
      // Set the loading message for topster
      setLoadingTopsterMessage('Loading topster...');

      const topsterResponse = await fetch(`/api/get_topster/${username}/`);

      if (!topsterResponse.ok) {
        throw new Error('Oops, sorry about that, there was an internal error.');
      }

      const topsterBlob = await topsterResponse.blob();
      const imageUrl = URL.createObjectURL(topsterBlob);
      setTopsterImageUrl(imageUrl);
      setLoadingTopsterMessage('');

      setUsername('');
    } catch (error) {
      setValidationMessage(error.message);
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
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
      <form onSubmit={handleSubmit} className="username-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value.toLowerCase())}
          placeholder="Enter your username"
          required
          disabled={isLoading}
          className="username-input"
        />
        {!isLoading && <button type="submit" className="submit-button">Submit</button>}
      </form>
      {validationMessage && <p className="validation-message">{validationMessage}</p>}
      {loadingStatsMessage && <p className="loading-message">{loadingStatsMessage}</p>}
      {loadingTopsterMessage && <p className="loading-message">{loadingTopsterMessage}</p>}

      {statsString && (
        <div className="stats-container">
          <h3>Stats String:</h3>
          <div className="stats-content" dangerouslySetInnerHTML={{ __html: statsString }} />
        </div>
      )}

      {topsterImageUrl && (
        <div className="topster-container">
          <h3>User Topster:</h3>
          <img 
            src={topsterImageUrl} 
            alt="User Topster" 
            className="topster-image"
          />
        </div>
      )}
    </div>
  );
};

export default HomePage;
