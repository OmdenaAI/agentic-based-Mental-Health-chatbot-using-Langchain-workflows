import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SurveyWizard from './pages/SurveyWizard';
import ModeSelector from './pages/ModeSelector';
import Chat from './pages/Chat';
import ProfileFeedback from './pages/ProfileFeedback';
import Dashboard from './pages/Dashboard';
import GeneralPage from './pages/GeneralPage';
import ConsentGate from './pages/ConsentGate';
import ThirdPartyAuth from './pages/ThirdPartyAuth';



function App() {
  return (
    <Router>
      <Routes>
        {/* Default landing page now points to general menu */}
        <Route path="/" element={<GeneralPage />} />

        <Route path="/survey" element={<SurveyWizard />} />
        <Route path="/profile-feedback" element={<ProfileFeedback />} />
        <Route path="/select-mode" element={<ModeSelector />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/home" element={<GeneralPage />} />
        <Route path="/consent-gate" element={<ConsentGate />} />
        <Route path="/third-party-auth" element={<ThirdPartyAuth />} />
        
      </Routes>
    </Router>
  );
}

export default App;
