import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Start() {
  const [consent, setConsent] = useState(false);
  const [mode, setMode] = useState('text');
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();

  const startSession = async () => {
    if (!consent || !userId) return alert('Please provide consent and ID');

    try {
      await axios.post('http://localhost:8000/init_session', {
        user_id: userId,
        consent,
        mode
      });
      localStorage.setItem('user_id', userId);
      localStorage.setItem('mode', mode);
      navigate('/chat');
    } catch (err) {
      alert('Could not start session. Please check backend is running.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Welcome to the Mental Health Assistant</h2>
      <input
        placeholder="Enter your name or ID"
        onChange={e => setUserId(e.target.value)}
      />
      <br />
      <label>
        <input
          type="checkbox"
          onChange={e => setConsent(e.target.checked)}
        />
        I agree to the terms and privacy policy
      </label>
      <br />
      <label>
        <input
          type="radio"
          name="mode"
          value="text"
          checked={mode === 'text'}
          onChange={() => setMode('text')}
        />
        Text Mode
      </label>
      <label>
        <input
          type="radio"
          name="mode"
          value="voice"
          checked={mode === 'voice'}
          onChange={() => setMode('voice')}
        />
        Voice Mode
      </label>
      <br />
      <button onClick={startSession}>Start</button>
    </div>
  );
}
