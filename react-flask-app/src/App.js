import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

import logo from './logo.svg';
import './App.css';
import UserDiary from './components/UserDiaryComponent'; // Adjust the import based on your file structure

function App() {
  const [currentTime, setCurrentTime] = useState(0);
  const [username, setUsername] = useState('');
  const [users, setUsers] = useState([]);
  const [userData, setUserData] = useState([]);
  const [validationMessage, setValidationMessage] = useState('');

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
    
    // Clear previous user data when searching for a new user
    setUserData([]);
    setValidationMessage('');
    
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
      setValidationMessage(data.message); // Show success message
  
      // Update the user data state with the diary entries
      setUserData(data.user_data);
  
      // Optionally clear the input after successful submission
      setUsername(''); 
    })
    .catch(error => {
      setValidationMessage(error.message); // Show error message
      console.error('Error:', error);
    });
  };

  return (
    <Router>
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
          {validationMessage && <p>{validationMessage}</p>}
          <h2>The current time is {currentTime}.</h2>
          <h3>Users:</h3>
          <ul>
            {users.length > 0 ? (
              users.map(user => (
                <li key={user.id}>
                  <Link to={`/user-diary/${user.username}`}>{user.username}</Link>
                </li>
              ))
            ) : (
              <li>No users found.</li>
            )}
          </ul>
          <Routes>
            <Route path="/user-diary/:username" element={<UserDiary />} />
          </Routes>

        </header>
      </div>
    </Router>
  );
}

export default App;
