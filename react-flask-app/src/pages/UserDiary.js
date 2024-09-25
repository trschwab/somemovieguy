import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const UserDiary = () => {
  const { username } = useParams();
  const [diaryEntries, setDiaryEntries] = useState([]);
  
  useEffect(() => {
    fetch(`/api/user_diary/${username}/`)
      .then(res => res.json())
      .then(data => {
        setDiaryEntries(data.diary_entries);
      })
      .catch(error => {
        console.error('Error fetching user diary:', error);
      });
  }, [username]);

  return (
    <div>
      <h2>{username}'s Diary</h2>
      {diaryEntries.length > 0 ? (
        <table>
          <thead>
            <tr>
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
            {diaryEntries.map((entry, index) => (
              <tr key={index}>
                <td>{entry.day}</td>
                <td>{entry.month}</td>
                <td>{entry.year}</td>
                <td>{entry.film}</td>
                <td>{entry.released}</td>
                <td>{entry.rating}</td>
                <td><a href={entry.review_link}>Review</a></td>
                <td><a href={entry.film_link}>Film Link</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No diary entries found.</p>
      )}
    </div>
  );
};

export default UserDiary;
