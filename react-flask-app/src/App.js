import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

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
      setValidationMessage(data.message); // Success message
      setUsername(''); // Clear the input

      // Fetch updated users list after adding a new user
      setUsers(prevUsers => [...prevUsers, { username }]); // Add new user to the state

      // Display the user data (for example, setting it to state)
      setUserData(data.user_data); // Create a new state for user data
    })
    .catch(error => {
      setValidationMessage(error.message);
      console.error('Error:', error);
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
        {validationMessage && <p>{validationMessage}</p>}
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
        {userData.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Day</th>
                <th>Month</th>
                <th>Year</th>
                <th>Film</th>
                <th>Released</th>
                <th>Rating</th>
                <th>Review Link</th>
                <th>Film Link</th>
              </tr>
            </thead>
            <tbody>
              {userData.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.day}</td>
                  <td>{item.month}</td>
                  <td>{item.year}</td>
                  <td>{item.film}</td>
                  <td>{item.released}</td>
                  <td>{item.rating}</td>
                  <td><a href={item.review_link}>Review</a></td>
                  <td><a href={item.film_link}>Film Link</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </header>
    </div>
  );
}

export default App;
