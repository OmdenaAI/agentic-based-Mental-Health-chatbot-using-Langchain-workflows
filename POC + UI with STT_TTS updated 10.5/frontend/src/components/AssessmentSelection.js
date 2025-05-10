import React from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

const AssessmentSelection = () => {
  const navigate = useNavigate();
  const profile = JSON.parse(localStorage.getItem("user_profile")) || {};
  const selectedIssues = profile["Mental Health Issues"] || [];

  const handleStart = () => {
    if (selectedIssues.length === 0) {
      alert("No mental health issues selected. Please update your profile.");
      return;
    }
    localStorage.setItem("remaining_issues", JSON.stringify(selectedIssues));
    const first = selectedIssues[0].toLowerCase();
    navigate(`/assessment-${first}`);
  };

  return (
    <Card className="max-w-xl mx-auto mt-10 p-6 text-center">
      <h2 className="text-2xl font-semibold mb-2 text-green-700">Assessment Selection</h2>
      <p className="mb-4 text-gray-700">Select an assessment based on your reported mental health issues</p>
      
      {selectedIssues.length > 0 ? (
        <div className="bg-gray-50 rounded-md p-4 mb-6">
          {selectedIssues.map((issue, index) => (
            <div key={index} className="text-gray-800 font-medium">• {issue}</div>
          ))}
        </div>
      ) : (
        <p className="text-red-500">No issues selected. Please go back and update.</p>
      )}

      <Button onClick={handleStart}>Start Assessment</Button>
    </Card>
  );
};

export default AssessmentSelection;
