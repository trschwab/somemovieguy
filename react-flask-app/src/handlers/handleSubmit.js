const handleSubmit = (e) => {
    e.preventDefault();
    setValidationMessage('This might take a few minutes...');
  
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
        setValidationMessage(data.message);
        setUserData(data.user_data);
        setUsername('');
      })
      .catch(error => {
        setValidationMessage(error.message);
        console.error('Error:', error);
      });
  };

export default handleSubmit;