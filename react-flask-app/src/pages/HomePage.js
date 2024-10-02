import React, { useState } from 'react';
import handleSubmit from '../handlers/handleSubmit';
import handleGetStats from '../handlers/handleGetStats';
import handleGetTopster from '../handlers/handleGetTopster';
import handleGetStatsStr from '../handlers/handleGetStatsStr';
import handleGetMovies from '../handlers/handleGetMovies';

const HomePage = () => {
  const [username, setUsername] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [userData, setUserData] = useState([]);
  const [stats, setStats] = useState(null);
  const [topsterImageUrl, setTopsterImageUrl] = useState('');
  const [statsString, setStatsString] = useState('');
  const [movieData, setMovieData] = useState([]);

  const formatStatsString = (str) => {
    return str.split('\n').map((line, index) => (
      <span key={index}>
        {line}
        <br />
      </span>
    ));
  };

  const handleFormSubmit = (e) => {
    handleSubmit(e, username, setValidationMessage, setUserData, setUsername);
  };

  const handleStatsButtonClick = () => {
    handleGetStats(username, setValidationMessage, setStats);
  };

  const handleTopsterButtonClick = () => {
    handleGetTopster(username, setValidationMessage, setTopsterImageUrl);
  };

  const handleStatsStringButtonClick = () => {
    handleGetStatsStr(username, setValidationMessage, setStatsString);
  };

  const handleMoviesButtonClick = () => {
    handleGetMovies(setValidationMessage, setMovieData);
  };

  return (
    <div className="HomePage">
      <form onSubmit={handleFormSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value.toLowerCase())}
          placeholder="Enter username"
          required
        />
        <button type="submit">Add User</button>
      </form>
      {validationMessage && <p>{validationMessage}</p>}

      {/* Button to get stats */}
      <button onClick={handleStatsButtonClick}>Get Stats</button>
      {stats && (
        <div>
          <h3>User Stats:</h3>
          {stats.length > 0 && (
            <table>
              <thead>
                <tr>
                  <th>Day</th>
                  <th>Month</th>
                  <th>Year</th>
                  <th>Film</th>
                  <th>Released</th>
                  <th>Rating</th>
                  <th>Review Link</th>
                  <th>Film Link</th>
                  <th>Director</th>
                  <th>Movie Rating</th>
                  <th>Movie URL</th>
                  <th>Image</th>
                </tr>
              </thead>
              <tbody>
                {stats.map((item, index) => (
                  <tr key={index}>
                    <td>{item.day}</td>
                    <td>{item.month}</td>
                    <td>{item.year}</td>
                    <td>{item.film}</td>
                    <td>{item.released}</td>
                    <td>{item.rating}</td>
                    <td><a href={item.review_link}>Review</a></td>
                    <td><a href={item.film_link}>Film Link</a></td>
                    <td>{item.director}</td>
                    <td>{item.rating_value}</td>
                    <td><a href={item.url}>Movie Link</a></td>
                    <td><img src={item.image} alt={item.film} width="50" /></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Button to get stats string */}
      <button onClick={handleStatsStringButtonClick}>Get Stats String</button>
      {statsString && (
        <div>
          <h3>Stats String:</h3>
          <div dangerouslySetInnerHTML={{ __html: statsString }} />
        </div>
      )}

      {/* Button to get user topster */}
      <button onClick={handleTopsterButtonClick}>Get User Topster</button>
      {validationMessage && <p>{validationMessage}</p>}
      {topsterImageUrl && (
        <div>
          <h3>User Topster:</h3>
          <img 
            src={topsterImageUrl} 
            alt="User Topster" 
            style={{ 
              maxHeight: '100vh', // Limit the height to the viewport height
              width: 'auto', // Maintain aspect ratio by adjusting width automatically
              display: 'block', // Prevent inline spacing issues
              margin: '0 auto' // Center the image horizontally
            }} 
          />
        </div>
      )}

      {/* Button to fetch and display movie table */}
      <button onClick={handleMoviesButtonClick}>Get Movies</button>
      {movieData.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Director</th>
              <th>Rating</th>
              <th>Released</th>
              <th>URL</th>
            </tr>
          </thead>
          <tbody>
            {movieData.map((movie, index) => (
              <tr key={index}>
                <td><img src={movie.image} alt={movie.name} width="50" /></td>
                <td>{movie.name}</td>
                <td>{movie.director}</td>
                <td>{movie.rating_value}</td>
                <td>{movie.released_event}</td>
                <td><a href={movie.url}>Movie Link</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default HomePage;
