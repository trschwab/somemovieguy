// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import StatsPage from './pages/StatsPage';
import UserDiaryPage from './pages/UserDiary';
import AboutPage from './pages/AboutPage'; // Importing the AboutPage component

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/stats" element={<StatsPage />} />
        <Route path="/UserDiary" element={<UserDiaryPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Router>
  );
}

export default App;
