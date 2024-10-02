const handleGetStatsStr = () => {
    setValidationMessage('');
    if (!username) {
      setValidationMessage('Please enter a username first!');
      return;
    }

    fetch(`/api/user_stats_string/${username}/`)
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || 'Something went wrong');
          });
        }
        return response.json();
      })
      .then(data => {
        console.log('Stats String Data:', data);
        setStatsString(JSON.stringify(data.return_string, null, 2));
      })      
      .catch(error => {
        setValidationMessage(error.message);
        console.error('Error:', error);
      });
  };

export default handleGetStatsStr;