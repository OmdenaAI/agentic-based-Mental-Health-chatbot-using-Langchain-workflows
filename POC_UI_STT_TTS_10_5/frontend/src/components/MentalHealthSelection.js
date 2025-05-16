import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

const issues = ["Depression", "Anxiety", "Stress", "Social Media FOMO"];

const MentalHealthSelection = () => {
  const navigate = useNavigate();
  const [selectedIssues, setSelectedIssues] = useState([]);
  const [selectedState, setSelectedState] = useState("");

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    setSelectedIssues((prev) =>
      checked ? [...prev, value] : prev.filter((i) => i !== value)
    );
  };

  const handleNext = () => {
    if (selectedIssues.length === 0 || !selectedState) {
      alert("Please select at least one issue and your mental health state.");
      return;
    }
    localStorage.setItem("mental_health_issues", JSON.stringify(selectedIssues));
    localStorage.setItem("mental_health_state", selectedState);
    navigate("/privacy-consent");
  };

  return (
    <Card className="max-w-md mx-auto mt-10 p-6 rounded-xl shadow-md bg-white">
      <h2 className="text-2xl font-semibold text-teal-800 mb-1">User Information</h2>
      <p className="text-sm text-gray-600 mb-4">Step 2 of 3: Mental Health</p>
      <div className="w-full bg-gray-200 h-2 rounded-full mb-6">
        <div className="bg-teal-600 h-2 rounded-full" style={{ width: "66%" }}></div>
      </div>

      <div className="mb-6">
        <label className="block font-medium mb-2">Mental Health Issues (select all that apply)</label>
        <div className="space-y-2">
          {issues.map((issue) => (
            <div key={issue} className="flex items-center gap-2">
              <input
                type="checkbox"
                id={issue}
                value={issue}
                checked={selectedIssues.includes(issue)}
                onChange={handleCheckboxChange}
                className="accent-teal-600"
              />
              <label htmlFor={issue}>{issue}</label>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-6">
        <label className="block font-medium mb-2">Current Mental Health State</label>
        <select
          value={selectedState}
          onChange={(e) => setSelectedState(e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          <option value="">How would you describe your current mental health?</option>
          <option value="Excellent">Excellent</option>
          <option value="Good">Good</option>
          <option value="Fair">Fair</option>
          <option value="Poor">Poor</option>
          <option value="At Risk">At Risk</option>
          <option value="In Crisis">In Crisis</option>
        </select>
      </div>

      <div className="flex justify-between">
        <Button variant="outline" onClick={() => navigate("/user-info")}>
          Back
        </Button>
        <Button onClick={handleNext}>Next</Button>
      </div>
    </Card>
  );
};

export default MentalHealthSelection;
