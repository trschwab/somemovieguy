import React, { useState } from 'react';

const HomePage = () => {
  const [username, setUsername] = useState('');
  const [validationMessage, setValidationMessage] = useState('');
  const [userData, setUserData] = useState([]);
  const [stats, setStats] = useState(null); // To hold the statistics
  const [movieData, setMovieData] = useState([]); // To hold the movie data

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidationMessage('');

    fetch('/api/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username }),
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.message || 'Something went wrong');
        });
      }
      return response.json();
    })
    .then(data => {
      console.log(data);
      setValidationMessage(data.message); // Show success message
      setUserData(data.user_data); // Update state with the user's diary entries
      setUsername(''); // Clear input after submission
    })
    .catch(error => {
      setValidationMessage(error.message); // Show error message
      console.error('Error:', error);
    });
  };

  const handleGetStats = () => {
    setValidationMessage('');
    if (!username) {
      setValidationMessage('Please enter a username first!');
      return;
    }
  
    fetch(`/api/user_diary_combined/${username}/`)
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || 'Something went wrong');
          });
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
        setStats(data.combined_data); // Update stats state with the combined data
      })
      .catch(error => {
        setValidationMessage(error.message); // Show error message
        console.error('Error:', error);
      });
  };
  

  // Fetch movie data
  const handleGetMovies = () => {
    fetch('/api/movies/') // Assuming your Flask API has this endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch movies.');
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
        setMovieData(data.movies); // Assuming the movie data is under 'movies'
      })
      .catch(error => {
        setValidationMessage(error.message); // Show error message
        console.error('Error:', error);
      });
  };

  return (
    <div className="HomePage">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
          required
        />
        <button type="submit">Add User</button>
      </form>
      {validationMessage && <p>{validationMessage}</p>}
      {userData.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Day</th>
              <th>Month</th>
              <th>Year</th>
              <th>Film</th>
              <th>Released</th>
              <th>Rating</th>
              <th>Review Link</th>
              <th>Film Link</th>
            </tr>
          </thead>
          <tbody>
            {userData.map((item, index) => (
              <tr key={index}>
                <td>{item.name}</td>
                <td>{item.day}</td>
                <td>{item.month}</td>
                <td>{item.year}</td>
                <td>{item.film}</td>
                <td>{item.released}</td>
                <td>{item.rating}</td>
                <td><a href={item.review_link}>Review</a></td>
                <td><a href={item.film_link}>Film Link</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <button onClick={handleGetStats}>Get Stats</button>
      {stats && (
        <div>
          <h3>User Stats:</h3>
          {stats && stats.length > 0 && (
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

      {/* Button to fetch and display movie table */}
      <button onClick={handleGetMovies}>Get Movies</button>
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
