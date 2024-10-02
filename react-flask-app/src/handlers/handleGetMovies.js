const [movieData, setMovieData] = useState([]);

const handleGetMovies = () => {
    fetch('/api/movies/')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch movies.');
        }
        return response.json();
      })
      .then(data => {
        console.log(data);
        setMovieData(data.movies);
      })
      .catch(error => {
        setValidationMessage(error.message);
        console.error('Error:', error);
      });
  };

export default handleGetMovies;