// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserInfo from "./components/UserInfo";
import MentalHealthSelection from "./components/MentalHealthSelection";
import PrivacyConsent from "./components/PrivacyConsent";
import Profile from "./components/Profile";
import AssessmentSelection from "./components/AssessmentSelection";
import AssessmentDepression from "./components/AssessmentDepression";
import AssessmentAnxiety from "./components/AssessmentAnxiety";
import AssessmentStress from "./components/AssessmentStress";
import AssessmentFOMO from "./components/AssessmentFOMO";
import ChatPage from "./components/ChatPage";
import LandingPage from "./components/LandingPage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/user-info" element={<UserInfo />} />
        <Route path="/mental-health" element={<MentalHealthSelection />} />
        <Route path="/privacy-consent" element={<PrivacyConsent />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/assessment-selection" element={<AssessmentSelection />} />
        <Route path="/assessment-depression" element={<AssessmentDepression />} />
        <Route path="/assessment-anxiety" element={<AssessmentAnxiety />} />
        <Route path="/assessment-stress" element={<AssessmentStress />} />
        <Route path="/assessment-fomo" element={<AssessmentFOMO />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </Router>
  );
};

export default App;


