import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './HomePage.css';
import './styles_v2.css';
import styles from './styles';
import StatsComponent from "../components/StatsComponent";

const StatsPage = () => {
  const [username, setUsername] = useState('');
  const [watchlistUsername, setWatchlistUsername] = useState(''); // State for watchlist username
  const [validationMessage, setValidationMessage] = useState('');
  const [messageClass, setMessageClass] = useState('');
  const [userData, setUserData] = useState([]);
  const [statsString, setStatsString] = useState('');
  const [topsterImageUrl, setTopsterImageUrl] = useState('');
  const [watchlist, setWatchlist] = useState([]);  // State for user's watchlist
  const [randomMovie, setRandomMovie] = useState(null); // State for random movie
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

  const handleGetWatchlist = async (e) => {
    e.preventDefault();

    if (!watchlistUsername) {
      setValidationMessage('Please enter a username for the watchlist.');
      setMessageClass('validation-message-red');
      return;
    }

    try {
      setIsLoading(true);
      const watchlistResponse = await fetch(`/api/user_watchlist/${watchlistUsername}/`);

      if (!watchlistResponse.ok) {
        throw new Error('Error fetching watchlist.');
      }

      const watchlistData = await watchlistResponse.json();

      // Check if the watchlist is empty
      if (watchlistData.length === 0) {
        setValidationMessage('Watchlist is empty.');
        setMessageClass('validation-message-red');
        return;
      }

      // Set the user's watchlist
      setWatchlist(watchlistData);
      setValidationMessage('');
      setMessageClass('');

      // Fetch a random movie from the watchlist using the new endpoint
      const randomMovieResponse = await fetch(`/api/random_watchlist_movie/${watchlistUsername}/`);

      if (!randomMovieResponse.ok) {
        throw new Error('Error fetching random movie from watchlist.');
      }

      const randomMovieData = await randomMovieResponse.json();

      // Display the random movie
      setValidationMessage(`Random Movie: ${randomMovieData.title}`);
      setMessageClass('validation-message-green');
      setRandomMovie(randomMovieData); // Store the random movie in state
    } catch (error) {
      console.error('Error fetching watchlist:', error);
      setValidationMessage('Failed to fetch watchlist.');
      setMessageClass('validation-message-red');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
      <h2>Enter your Letterboxd username for a Topster:</h2>
      <form onSubmit={handleSubmit} className="username-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value.toLowerCase())}
          placeholder="Username"
          required
          disabled={isLoading}
          className="username-input"
        />
        {!isLoading && <button type="submit" className="submit-button">Submit</button>}
      </form>
      {validationMessage && <p className={`validation-message ${messageClass}`}>{validationMessage}</p>}
      {loadingTopsterMessage && <p className="loading-message">{loadingTopsterMessage}</p>}

      {/* New Input Box for Watchlist Username */}
      <form onSubmit={handleGetWatchlist} className="username-form">
        <input
          type="text"
          value={watchlistUsername}
          onChange={(e) => setWatchlistUsername(e.target.value.toLowerCase())}
          placeholder="Enter username for watchlist"
          required
          disabled={isLoading}
          className="username-input"
        />
        {!isLoading && <button type="submit" className="submit-button">Get Watchlist</button>}
      </form>

      {/* Displaying the Watchlist */}
      {watchlist.length > 0 && (
        <div className="watchlist-container">
          <h3>Watchlist for {watchlistUsername}:</h3>
          <ul>
            {watchlist.map((movie, index) => (
              <li key={index}>
                <p>Title: {movie.title}</p>
                <p>Film URL: <a href={movie.film_url} target="_blank" rel="noopener noreferrer">{movie.film_url}</a></p>
                <img src={movie.poster_url} alt={movie.title} className="watchlist-movie-poster" />
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Display the Random Movie */}
      {randomMovie && (
        <div className="random-movie-container">
          <h3>Random Movie:</h3>
          <p>Title: {randomMovie.title}</p>
          <p>Film URL: <a href={randomMovie.film_url} target="_blank" rel="noopener noreferrer">{randomMovie.film_url}</a></p>
          <img src={randomMovie.poster_url} alt={randomMovie.title} className="random-movie-poster" />
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
