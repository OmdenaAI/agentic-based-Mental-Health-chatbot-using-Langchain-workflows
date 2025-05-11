import React from "react";
import { Link } from "react-router-dom";
import conversation from "./assets/converse.jpg";

export default function Assessmentmodal({ onClose }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      {/* Blurred background image layer */}
      <div
        className="absolute inset-0 bg-black"
        style={{
          backgroundImage: `url(${conversation})`,
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
        Let's start with a warm-up conversation :)
        </p>
        <p className="text-gray-500 rounded-lg bg-green-200 mb-6 p-4">
          Hi there! I'm GreenLife, your mental health companion. I'm here to
          listen, support, and provide resources to help you navigate your
          mental health journey. Before we dive deeper, I'd like to ask a few
          questions to better understand how I can support you. Everything you
          share is confidential and protected. You're in a safe space.
        </p>

        <Link to="/assessment">
          <button
            className="bg-green-400 cursor-pointer text-white py-2 px-4 rounded-xl hover:bg-green-600 mb-4"
            onClick={onClose}
          >
            Let us have a conversation
          </button>
        </Link>

        <p className="text-xs text-gray-500"></p>
      </div>
    </div>
  );
}
