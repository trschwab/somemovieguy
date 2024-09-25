import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserDiary = ({ username }) => {
  const [diaryEntries, setDiaryEntries] = useState([]);
  const [topMovies, setTopMovies] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserDiary = async () => {
      try {
        const response = await axios.get(`/api/user_diary/${username}/`);
        setDiaryEntries(response.data.diary_entries);
        setTopMovies(response.data.top_movies);
      } catch (err) {
        setError(err.response?.data?.message || 'An error occurred while fetching data.');
      }
    };

    fetchUserDiary();
  }, [username]);

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>{username}'s Diary Entries</h2>
      {diaryEntries.length > 0 ? (
        <ul>
          {diaryEntries.map((entry, index) => (
            <li key={index}>
              <strong>{entry.film}</strong> - Rated: {entry.rating} on {entry.day} {entry.month} {entry.year}
              <br />
              <a href={entry.review_link} target="_blank" rel="noopener noreferrer">View Review</a>
              <br />
              <a href={entry.film_link} target="_blank" rel="noopener noreferrer">View Film</a>
            </li>
          ))}
        </ul>
      ) : (
        <p>No diary entries found.</p>
      )}

      <h2>Top 20 Rated Movies</h2>
      {topMovies.length > 0 ? (
        <ul>
          {topMovies.map((movie, index) => (
            <li key={index}>
              <strong>{movie.film}</strong> - Rating: {movie.rating}
            </li>
          ))}
        </ul>
      ) : (
        <p>No top movies found.</p>
      )}
    </div>
  );
};

export default UserDiary;
