import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import './styles_v2.css';
import styles from './styles';
import StatsComponent from "../components/StatsComponent";


const StatsPage = () => {
  const [username, setUsername] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [messageClass, setMessageClass] = useState('');
  const [userData, setUserData] = useState([]);
  const [statsString, setStatsString] = useState('');
  const [topsterImageUrl, setTopsterImageUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStatsMessage, setLoadingStatsMessage] = useState('');
  const [loadingTopsterMessage, setLoadingTopsterMessage] = useState('');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Reset previous states
    setStatsString('');
    setTopsterImageUrl('');
    setValidationMessage('This might take a few minutes...');
    setMessageClass('');
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
      setUserData(userData.user_data);
      setValidationMessage(userData.message);
      setMessageClass('validation-message-green');

      // Load stats
      setLoadingStatsMessage('Loading stats...');
      const statsResponse = await fetch(`/api/user_stats_string/${username}/`);

      if (!statsResponse.ok) {
        throw new Error('Oops, sorry about that, there was an internal error.');
      }

      const statsData = await statsResponse.json();
      setStatsString(JSON.stringify(statsData.return_string, null, 2));
      setLoadingStatsMessage('');
      
      // Load topster
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
      setMessageClass('validation-message-red');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
      <p>test</p>
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
      {validationMessage && <p className={`validation-message ${messageClass}`}>{validationMessage}</p>}
      {loadingStatsMessage && <p className="loading-message">{loadingStatsMessage}</p>}
      {loadingTopsterMessage && <p className="loading-message">{loadingTopsterMessage}</p>}

      {/* {statsString && (
        <div className="stats-container">
          <h3>Stats String:</h3>
          
          <div className="stats-content" dangerouslySetInnerHTML={{ __html: statsString }} />
        </div>
      )}

      <StatsComponent username={username} /> */}

      {statsString && (
        <div className="stats-container">
          <h3>Stats String:</h3>
          <StatsComponent stats={statsString} />
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

export default StatsPage;
