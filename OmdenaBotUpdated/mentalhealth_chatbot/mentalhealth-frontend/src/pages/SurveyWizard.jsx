import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

// Consider whether the GeneralPage-style layout (calming, modern UI with navigation buttons)
// might be a better default entry point for user experience when launching the app.

export default function SurveyWizard({ skipToConsent }) {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);

  const [formData, setFormData] = useState({
    user_id: '',
    age: '',
    gender: '',
    employment_status: '',
    financial_worries: '',
    mental_issues: [],
    consent: false,
    consent_recording: false,
  });

  const steps = ['User Info', 'Mental Health', 'Consent & Submit'];

  const handleChange = (field) => (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleMultiCheckbox = (issue) => {
    setFormData((prev) => {
      const exists = prev.mental_issues.includes(issue);
      return {
        ...prev,
        mental_issues: exists
          ? prev.mental_issues.filter((i) => i !== issue)
          : [...prev.mental_issues, issue],
      };
    });
  };

  const next = () => setStep((s) => Math.min(s + 1, steps.length - 1));
  const back = () => setStep((s) => Math.max(s - 1, 0));

  const submit = async () => {
    if (!formData.consent || !formData.consent_recording) {
      alert('Please provide all required consents to proceed.');
      return;
    }
    try {
      await axios.post('https://ortal.ngrok.io/user_profile', formData);
      localStorage.setItem('user_id', formData.user_id);
      localStorage.setItem('user_profile', JSON.stringify(formData));
      navigate('/profile-feedback');
    } catch (err) {
      alert('Submission failed. Is the backend running?');
    }
  };

  const skip = () => {
    if (skipToConsent) {
      skipToConsent();
    } else {
      navigate('/home');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>{steps[step]}</h2>

      {step === 0 && (
        <>
          <input placeholder="Your name or ID" onChange={handleChange('user_id')} />
          <br />
          <input placeholder="Age" type="number" onChange={handleChange('age')} />
          <br />
          <select onChange={handleChange('gender')}>
            <option value="">Select gender</option>
            <option value="female">Female</option>
            <option value="male">Male</option>
            <option value="other">Other</option>
          </select>
          <br />
          <select onChange={handleChange('employment_status')}>
            <option value="">Employment status</option>
            <option value="student">Student</option>
            <option value="employed">Employed</option>
            <option value="unemployed">Unemployed</option>
            <option value="retired">Retired</option>
          </select>
          <br />
          <label>
            Are you worried about finances?
            <input type="text" onChange={handleChange('financial_worries')} />
          </label>
        </>
      )}

      {step === 1 && (
        <>
          <p>Select any mental health concerns:</p>
          {['anxiety', 'depression', 'stress', 'sleep issues', 'loneliness'].map((issue) => (
            <label key={issue} style={{ display: 'block' }}>
              <input
                type="checkbox"
                checked={formData.mental_issues.includes(issue)}
                onChange={() => handleMultiCheckbox(issue)}
              />
              {issue}
            </label>
          ))}
        </>
      )}

      {step === 2 && (
        <>
          <h4>Please confirm:</h4>
          <label>
            <input
              type="checkbox"
              checked={formData.consent}
              onChange={handleChange('consent')}
            />
            I consent to participate and share my data for support purposes.
          </label>
          <br />
          <label>
            <input
              type="checkbox"
              checked={formData.consent_recording}
              onChange={handleChange('consent_recording')}
            />
            I understand that this conversation may be recorded and shared with authorized third parties.
          </label>
        </>
      )}

      <br />
      <button onClick={back} disabled={step === 0}>
        Back
      </button>
      {step < steps.length - 1 ? (
        <button onClick={next}>Next</button>
      ) : (
        <button onClick={submit}>Submit</button>
      )}

      <br />
      <button onClick={skip} style={{ marginTop: '1rem', background: '#ddd' }}>
        ⏭️ Skip and Continue
      </button>
    </div>
  );
}
