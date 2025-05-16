import { useNavigate } from 'react-router-dom';
import './general.css';
import { useState } from 'react';
import SurveyWizard from './SurveyWizard';

export default function GeneralPage() {
  const navigate = useNavigate();
  const [showSurvey, setShowSurvey] = useState(false);

  const handleChatClick = () => {
    setShowSurvey(true);
  };

  const handleSkipSurvey = () => {
    setShowSurvey(false);
    navigate('/consent-gate');
  };

  return (
    <div className="general-wrapper">
      <header>
        <h1>🌿 OmdenaBot</h1>
        <p>Your well-being companion</p>
      </header>

      {showSurvey ? (
        <SurveyWizard skipToConsent={handleSkipSurvey} />
      ) : (
        <div className="button-panel">
          <button onClick={handleChatClick}>🗨️ Start Chat</button>
          <button onClick={() => navigate('/dashboard')}>📊 View Dashboard</button>
          <button onClick={() => navigate('/exercise')}>🧘 Exercises</button>
          <button onClick={() => navigate('/survey')}>📝 Start Survey</button>
          <button disabled>➕ Coming Soon</button>
        </div>
      )}
    </div>
  );
}