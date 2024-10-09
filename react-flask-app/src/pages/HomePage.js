import React, { useEffect, useState } from "react";
import BasicExample from '../components/NavbarComponent';

const HomePage = () => {
  const [movies, setMovies] = useState([]);

  // Array of specific movie titles you want to display
  const selectedMovieTitles = [
    'Magnolia',
    'Stop Making Sense',
    'Days of Heaven',
    'Koyaanisqatsi',
    'Superbad',
    'The Incredibles',
    'Three Colours: Blue',
    'Chungking Express',
    'Paris, Texas',
    'Amadeus',
    'Stalker',
    'Mishima: A Life in Four Chapters',
    'Where Is the Friend\'s House?',
    'Three Colours: Red',
    'When Harry Met Sally…',
    'Fallen Angels',
    'Wet Hot American Summer',
    'Jurassic Park',
    'Maelström',
    'Carts of Darkness',
    'The Great Beauty',
    'Portrait of a Lady on Fire',
    'Incendies',
    'La Haine',
    'Possum',
    'The Darjeeling Limited',
    'The Hand of God',
    'Singin\' in the Rain',
  ];

  useEffect(() => {
    fetch('/api/movies/')
      .then(response => response.json())
      .then(data => {
        if (data.movies) {
          // Filter the movies to match the titles in `selectedMovieTitles`
          const filteredMovies = data.movies.filter(movie => 
            selectedMovieTitles.includes(movie.name)
          );
          setMovies(filteredMovies);
        }
      })
      .catch(error => console.error("Error fetching movies:", error));
  }, []);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '20px',
      backgroundColor: '#f5f5f5',
      minHeight: '100vh'
    }}>
      <BasicExample />

      {/* Main Content */}
      <div style={{ width: '80%' }}>
        <div style={{
          textAlign: 'center',
          marginBottom: '20px',
          padding: '10px',
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.2)',
          borderRadius: '8px'
        }}>
          {/* <p style={{
            fontSize: '24px',
            fontWeight: 'bold',
            margin: 0
          }}>
            Selected Movies with Cool Animation
          </p> */}
        </div>

        {/* Display movie images with animations */}
        <div style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          gap: '20px',
        }}>
          {movies.length > 0 ? (
            movies.map((movie, index) => (
              <div
                key={index}
                style={{
                  position: 'relative',
                  width: '200px',
                  height: '300px',
                  overflow: 'hidden',
                  textAlign: 'center',
                  borderRadius: '8px',
                  boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.2)',
                  transform: 'scale(1)',
                  transition: 'transform 0.3s ease-in-out',
                  animation: `fadeIn 0.5s ease-in-out ${index * 0.2}s forwards`,
                  opacity: 0
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.transform = 'scale(1.05)';
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.transform = 'scale(1)';
                }}
              >
                <img
                  src={movie.image}
                  alt={movie.name}
                  style={{
                    width: '100%',
                    height: '100%',
                    objectFit: 'cover',
                    borderRadius: '8px'
                  }}
                />
                {/* <p style={{
                  position: 'absolute',
                  bottom: '10px',
                  left: 0,
                  right: 0,
                  margin: 0,
                  color: 'white',
                  fontWeight: 'bold',
                  fontSize: '16px',
                  backgroundColor: 'rgba(0, 0, 0, 0.6)',
                  padding: '5px',
                  borderRadius: '0 0 8px 8px'
                }}>
                  {movie.name}
                </p> */}
              </div>
            ))
          ) : (
            <p>Loading movies or no movies matched...</p>
          )}
        </div>
      </div>

      {/* Keyframe animation */}
      <style>
        {`
          @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
          }
        `}
      </style>
    </div>
  );
};

export default HomePage;
