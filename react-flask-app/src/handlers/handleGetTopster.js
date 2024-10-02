const handleGetTopster = () => {
    setValidationMessage('');
    if (!username) {
      setValidationMessage('Please enter a username first!');
      return;
    }
  
    fetch(`/api/get_topster/${username}/`)
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.message || 'Something went wrong');
          });
        }
        return response.blob();  // Get the response as a blob
      })
      .then(blob => {
        const imageUrl = URL.createObjectURL(blob);  // Create a URL for the image blob
        setTopsterImageUrl(imageUrl);  // Set the URL for the image
      })
      .catch(error => {
        setValidationMessage(error.message);
        console.error('Error:', error);
      });
  };

export default handleGetTopster;