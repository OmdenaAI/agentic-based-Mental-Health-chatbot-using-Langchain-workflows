import React from "react";
import { Link } from "react-router-dom";
import modal_background_image from "./assets/modal_background.jpg";

export default function GreenLifeModal({ onClose }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      {/* Blurred background image layer */}
      <div
        className="absolute inset-0 bg-black"
        style={{
          backgroundImage: `url(${modal_background_image})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "blur(5px)",
          zIndex: -1,
        }}
      ></div>

      {/* Modal content layer */}
      <div className="relative bg-white p-6 rounded-2xl shadow-lg max-w-md w-full text-center">
        <h2 className="text-2xl font-bold mb-2 text-green-500">GreenLife</h2>
        <p className="text-gray-700 mb-4">
          A safe space to talk about your mental health
        </p>
        <p className="text-gray-500 mb-6">
          Note: This is a mockup. GreenLife is not a replacement for
          professional mental health services. If you're experiencing a crisis,
          please contact emergency services or a mental health professional. .
        </p>

        <Link to="/onboarding">
          <button
            className="bg-green-500 text-white py-2 px-4 rounded-xl hover:bg-green-600 mb-4"
            onClick={onClose}
          >
            Get Started
          </button>
        </Link>

        <p className="text-xs text-gray-500"></p>
      </div>
    </div>
  );
}
