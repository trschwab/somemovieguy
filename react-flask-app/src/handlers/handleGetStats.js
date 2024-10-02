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
        setStats(data.combined_data);
      })
      .catch(error => {
        setValidationMessage(error.message);
        console.error('Error:', error);
      });
  };

export default handleGetStats;