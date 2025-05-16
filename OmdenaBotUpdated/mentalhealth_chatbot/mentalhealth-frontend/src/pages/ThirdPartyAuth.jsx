import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ThirdPartyAuth() {
  const navigate = useNavigate();
  const [isUnder18, setIsUnder18] = useState(null);
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');

  const handleContinue = () => {
    if (isUnder18 === null) {
      setError('Please select your age group.');
      return;
    }
    if (!phone) {
      setError('Please provide a phone number.');
      return;
    }

    localStorage.setItem('guardian_phone', phone);
    localStorage.setItem('is_under_18', isUnder18);
    navigate("/select-mode");
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h2>3rd Party Notification Setup</h2>
      <p>To ensure safety, we ask for a contact who will be notified in case of emotional distress.</p>

      <div style={{ marginBottom: '1rem' }}>
        <strong>Are you under 18?</strong>
        <div>
          <label>
            <input type="radio" name="age" onChange={() => setIsUnder18(true)} /> Yes
          </label>
          <label style={{ marginLeft: '1rem' }}>
            <input type="radio" name="age" onChange={() => setIsUnder18(false)} /> No
          </label>
        </div>
      </div>

      {isUnder18 !== null && (
        <div style={{ marginBottom: '1rem' }}>
          <label>
            {isUnder18
              ? 'Parent or Guardian Phone Number:'
              : 'Therapist (Optional) Phone Number:'}
            <br />
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="+1234567890"
              style={{ width: '100%', marginTop: '0.5rem' }}
            />
          </label>
        </div>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button onClick={handleContinue}>Continue to Chat</button>
    </div>
  );
}
