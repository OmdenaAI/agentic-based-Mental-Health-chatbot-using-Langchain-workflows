import { StrictMode } from 'react'
import {
  BrowserRouter as Router, Routes,
  Route
} from "react-router-dom";import { createRoot } from 'react-dom/client'
import './index.css'
import Hero from './hero.jsx'
import Chat from './chat.jsx'
import Modal from './modal.jsx'
import Onboarding from './onboarding.jsx';
import Assessmentmodal from './assessmentModal.jsx'
import Assessment from './assessment.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Hero/>} />
        <Route path="/chat" element={<Chat/>} />
        <Route path="/modal" element={<Modal/>} />
        <Route path="/onboarding" element={<Onboarding/>} />
        <Route path="/assessmentModal" element={<Assessmentmodal/>} />
        <Route path="/assessment" element={<Assessment/>} />

      </Routes>
    </Router>
  </StrictMode>,
)
