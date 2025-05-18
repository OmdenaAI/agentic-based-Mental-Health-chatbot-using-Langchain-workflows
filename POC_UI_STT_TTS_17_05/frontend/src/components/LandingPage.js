// LandingPage.js
import React from "react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-teal-50 to-cyan-100">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-lg w-full text-center">
        <h1 className="text-3xl font-extrabold text-teal-700 mb-2">Omdena-MindfulChat</h1>
        <p className="text-gray-700 mb-1">A safe space to talk about your mental health</p>
        <p className="text-gray-600 mb-6 text-lg">
          MindfulChat is here to provide support, resources,<br />
          and a listening ear when you need it.
        </p>

        <button
          onClick={() => navigate("/user-info")}
          className="bg-teal-600 hover:bg-teal-700 text-white font-medium py-2 px-6 rounded-md transition duration-200"
        >
          Get Started
        </button>

        <p className="text-xs text-gray-500 mt-6 leading-relaxed">
          Note: This is a mockup. MindfulChat is not a replacement for professional mental health services.
          If you're experiencing a crisis, please contact emergency services or a mental health professional.
        </p>
      </div>
    </div>
  );
};

export default LandingPage;
