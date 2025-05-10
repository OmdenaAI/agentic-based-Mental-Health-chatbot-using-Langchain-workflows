import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function ProfileFeedback() {
  const navigate = useNavigate();
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(true);

  // Get stored user data
  const profile = JSON.parse(localStorage.getItem('user_profile'));

  useEffect(() => {
    const getFeedback = async () => {
      try {
        const res = await axios.post('http://localhost:8000/profile_feedback', profile);
        setFeedback(res.data.feedback);
      } catch (err) {
        setFeedback('Error generating feedback. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    if (profile) {
      getFeedback();
    } else {
      setFeedback('No profile data found.');
      setLoading(false);
    }
  }, []);

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Your Personalized Feedback</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div>
          <p>{feedback}</p>
          <br />
          <button onClick={() => navigate('/select-mode')}>Continue to Chat</button>
        </div>
      )}
    </div>
  );
}
