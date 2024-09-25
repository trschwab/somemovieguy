import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [username, setUsername] = useState('');
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch the current time
    fetch('/api/time')
      .then(res => res.json())
      .then(data => {
        setCurrentTime(data.time);
      });

    // Fetch the list of users
    fetch('/api/users/')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
      });
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('/api/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      // Fetch updated users list after adding a new user
      return fetch('/api/users/');
    })
    .then(res => res.json())
    .then(data => {
      setUsers(data); // Update the users state with the new list
      setUsername(''); // Clear the input
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Third and final deployment test
        </p>
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
        <h2>The current time is {currentTime}.</h2>
        <h3>Users:</h3>
        <ul>
          {users.length > 0 ? (
            users.map(user => (
              <li key={user.id}>{user.username}</li>
            ))
          ) : (
            <li>No users found.</li>
          )}
        </ul>
      </header>
    </div>
  );
}

export default App;
