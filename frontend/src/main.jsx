import { StrictMode } from 'react'
import {
  BrowserRouter as Router, Routes,
  Route
} from "react-router-dom";import { createRoot } from 'react-dom/client'
import './index.css'
import Hero from './hero.jsx'
import Chat from './chat.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<Hero/>} />
        <Route path="/chat" element={<Chat/>} />
      </Routes>
    </Router>
  </StrictMode>,
)
