import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function ConsentGate() {
  const navigate = useNavigate();
  const [consent, setConsent] = useState(false);
  const [consentRecording, setConsentRecording] = useState(false);

  const handleSubmit = () => {
    if (!consent || !consentRecording) {
      alert('Please agree to all consents to continue.');
      return;
    }
    navigate('/third-party-auth');
  };

  return (
    <div style={{ padding: '2rem', maxWidth: '600px', margin: 'auto' }}>
      <h2>Consent Required</h2>
      <p>Please read and accept the following to continue to chat.</p>

      <label style={{ display: 'block', marginBottom: '1rem' }}>
        <input
          type="checkbox"
          checked={consent}
          onChange={(e) => setConsent(e.target.checked)}
        />{' '}
        I consent to participate and share my data for support purposes.
      </label>

      <label style={{ display: 'block', marginBottom: '1rem' }}>
        <input
          type="checkbox"
          checked={consentRecording}
          onChange={(e) => setConsentRecording(e.target.checked)}
        />{' '}
        I understand this conversation may be recorded and shared with authorized third parties.
      </label>

      <button onClick={handleSubmit} style={{ marginTop: '1rem' }}>
        Continue
      </button>
    </div>
  );
}
