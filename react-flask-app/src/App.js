// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MainStatsPage from './pages/MainStatsPage';
import StatsPage from './pages/StatsPage';
import UserDiaryPage from './pages/UserDiary';
import AboutPage from './pages/AboutPage';
import TopsterPage from './pages/TopsterPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/test/" element={<HomePage />} />
        <Route path="/test/stats" element={<StatsPage />} />
        <Route path="/" element={<MainStatsPage />} />
        <Route path="/test/UserDiary" element={<UserDiaryPage />} />
        <Route path="/test/about" element={<AboutPage />} />
        <Route path="/test/topster" element={<TopsterPage />} />
      </Routes>
    </Router>
  );
}

export default App;
