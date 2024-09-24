import React, { useState, useEffect } from 'react';

function App() {
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');
  const [usernames, setUsernames] = useState([]);

  // Fetch all usernames from the backend
  const fetchUsernames = async () => {
    const response = await fetch('http://localhost:5000/api/usernames');
    const data = await response.json();
    setUsernames(data);
  };

  useEffect(() => {
    fetchUsernames();
  }, []); // This runs once when the component is mounted

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5000/api/usernames', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: username }),
    });

    const data = await response.json();
    setMessage(data.message);

    // Refresh the list of usernames after a new one is added
    fetchUsernames();
  };

  return (
    <div className="App">
      <h1>Enter Your Username</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Enter username"
        />
        <button type="submit">Submit</button>
      </form>
      <p>{message}</p>

      <h2>Current Usernames:</h2>
      <ul>
        {usernames.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
