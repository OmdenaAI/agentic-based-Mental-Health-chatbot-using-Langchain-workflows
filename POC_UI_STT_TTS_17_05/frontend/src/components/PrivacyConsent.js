import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/Button";
import { Card } from "./ui/Card";

const PrivacyConsent = () => {
  const [consent, setConsent] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (!consent) {
      alert("You must give consent to proceed.");
      return;
    }

    try {
      const profile = JSON.parse(localStorage.getItem("user_profile")) || {};
      const mentalHealthIssues = localStorage.getItem("mental_health_issues");
      const mentalHealthState = localStorage.getItem("mental_health_state");

      profile["Consent Given"] = true;
      profile["Mental Health Issues"] = mentalHealthIssues
        ? JSON.parse(mentalHealthIssues)
        : [];
      profile["Current Mental Health State"] = mentalHealthState || "";

      localStorage.setItem("user_profile", JSON.stringify(profile));
      navigate("/profile");
    } catch (error) {
      console.error("Error storing profile:", error);
      alert("Something went wrong. Please try again.");
    }
  };

  return (
    <Card className="max-w-md mx-auto mt-10 p-6 rounded-xl shadow-md bg-white">
      <h2 className="text-2xl font-semibold text-teal-800 mb-1">User Information</h2>
      <p className="text-sm text-gray-600 mb-4">Step 3 of 3: Privacy & Consent</p>
      <div className="w-full bg-gray-200 h-2 rounded-full mb-6">
        <div className="bg-teal-600 h-2 rounded-full" style={{ width: "100%" }}></div>
      </div>

      <div className="bg-blue-100 text-blue-800 p-4 rounded mb-6 text-sm">
        <strong className="block mb-1 text-base">Privacy & Data Usage</strong>
        MindfulChat values your privacy. Your conversations are encrypted and stored securely.
        We use anonymized data to improve our service and provide better support. You can request
        deletion of your data at any time.
      </div>

      <div className="mb-6">
        <label className="flex items-start gap-2 text-sm">
          <input
            type="checkbox"
            checked={consent}
            onChange={() => setConsent(!consent)}
            className="mt-1 accent-teal-600"
          />
          <span>
            I consent to the storage and processing of my data as described in the privacy policy.
            I understand that MindfulChat is not a replacement for professional mental health services.
          </span>
        </label>
      </div>

      <div className="flex justify-between">
        <Button variant="outline" onClick={() => navigate("/mental-health")}>
          Back
        </Button>
        <Button onClick={handleSubmit}>Submit</Button>
      </div>
    </Card>
  );
};

export default PrivacyConsent;
