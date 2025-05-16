import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProfileFeedback = () => {
  const [feedback, setFeedback] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedProfile = localStorage.getItem('user_profile');
    const user_id = localStorage.getItem('user_id');

    if (!storedProfile || !user_id) {
      setError('⚠️ Missing profile data. Please return to the survey.');
      setLoading(false);
      return;
    }

    const profile = JSON.parse(storedProfile);

    axios.post('https://ortal.ngrok.io/profile_feedback', {
      user_id,
      ...profile
    })
    .then((res) => {
      setFeedback(res.data.feedback);
    })
    .catch((err) => {
      console.error('❌ Error in feedback:', err);
      setError('⚠️ Error generating feedback. Please try again later.');
    })
    .finally(() => {
      setLoading(false);
    });
  }, []);

  return (
    <div style={{ padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h2>🧠 Personalized Feedback</h2>
      {loading && <p>Loading your feedback...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {!loading && !error && (
        <div style={{
          background: '#f2f2f2',
          padding: '1.5rem',
          borderRadius: '10px',
          whiteSpace: 'pre-line'
        }}>
          {feedback}
        </div>
      )}
    </div>
  );
};

export default ProfileFeedback;
