import React, { useEffect, useState } from "react";
import './styles_v2.css';
import './topsterStyles.css';
import styles from './styles';
import BasicExample from '../components/NavbarComponent';

const TopsterPage = () => {
  const [movies, setMovies] = useState([]);
  const [selectedMovies, setSelectedMovies] = useState(Array(25).fill(null)); // 25 boxes for the 5x5 grid
  const [searchInputs, setSearchInputs] = useState(Array(25).fill('')); // Store search inputs for each grid item

  useEffect(() => {
    // Fetch movies from Flask API
    fetch('/api/movies/')
      .then(response => response.json())
      .then(data => {
        if (data.movies) {
          setMovies(data.movies);
        }
      })
      .catch(error => console.error('Error fetching movies:', error));
  }, []);

  // Handle input change for movie search
  const handleInputChange = (index, value) => {
    const newSearchInputs = [...searchInputs];
    newSearchInputs[index] = value;
    setSearchInputs(newSearchInputs);
  };

  // Handle selection of a movie
  const handleSelect = (index, movie) => {
    const newSelectedMovies = [...selectedMovies];
    newSelectedMovies[index] = movie;
    setSelectedMovies(newSelectedMovies);

    // Clear the search input after selection
    handleInputChange(index, '');
  };

  return (
    <div style={styles.container}>
      <BasicExample />

      <div style={styles.contentContainer}>
        <div className="grid-container">
          {Array(25).fill().map((_, index) => (
            <div className="grid-item" key={index}>
              {/* Movie Search Box */}
              <input
                type="text"
                value={searchInputs[index]}
                placeholder="Search for a movie"
                onChange={(e) => handleInputChange(index, e.target.value)}
                className="search-box"
              />

              {/* Show movie suggestions based on input */}
              {searchInputs[index] && (
                <div className="dropdown">
                  {movies
                    .filter(movie => movie.name.toLowerCase().includes(searchInputs[index].toLowerCase()))
                    .map((movie) => (
                      <div
                        key={movie.name}
                        className="dropdown-item"
                        onClick={() => handleSelect(index, movie)}
                      >
                        {movie.name}
                      </div>
                    ))}
                </div>
              )}

              {/* Display selected movie image */}
              {selectedMovies[index] && selectedMovies[index].image && (
                <img 
                  src={selectedMovies[index].image} 
                  alt={selectedMovies[index].name} 
                  style={{ width: '100%', height: 'auto' }}
                />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TopsterPage;
