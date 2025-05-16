import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import axios from 'axios';

export default function ModeSelector() {
  const [mode, setMode] = useState('text');
  const navigate = useNavigate();
  const user_id = localStorage.getItem('user_id');

  const startSession = async () => {
    if (!user_id) {
      alert('User ID not found. Please fill the survey first.');
      return;
    }

    try {
      await axios.post('http://localhost:8000/init_session', {
        user_id,
        consent: true,
        mode
      });

      localStorage.setItem('mode', mode);
      navigate('/chat');
    } catch (err) {
      alert('Could not start session. Make sure the backend is running.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Select Interaction Mode</h2>
      <p>Please choose how you'd like to chat with the assistant:</p>

      <label>
        <input
          type="radio"
          name="mode"
          value="text"
          checked={mode === 'text'}
          onChange={() => setMode('text')}
        />
        💬 Text Only
      </label>

      <br />

      <label>
        <input
          type="radio"
          name="mode"
          value="voice"
          checked={mode === 'voice'}
          onChange={() => setMode('voice')}
        />
        🗣️ Voice (STT + TTS)
      </label>

      <br />
      <button onClick={startSession} style={{ marginTop: '1rem' }}>
        Start Chat
      </button>
    </div>
  );
}
