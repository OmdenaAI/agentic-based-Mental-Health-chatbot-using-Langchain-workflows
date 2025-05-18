import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

const questions = [
  "I fear others have more rewarding experiences than me.",
  "I fear my friends have more rewarding lives than me.",
  "I get worried when I find out my friends are having fun without me.",
  "I get anxious when I don’t know what my friends are up to.",
  "Sometimes I wonder if I spend too much time keeping up with what’s going on."
];

const options = [
  "Not at all true",
  "Slightly true",
  "Moderately true",
  "Very true",
  "Extremely true"
];

const scoreMapping = {
  "Not at all true": 0,
  "Slightly true": 1,
  "Moderately true": 2,
  "Very true": 3,
  "Extremely true": 4
};

const AssessmentFOMO = () => {
  const navigate = useNavigate();
  const [answers, setAnswers] = useState(Array(questions.length).fill(""));
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [result, setResult] = useState("");

  const handleChange = (index, value) => {
    const updated = [...answers];
    updated[index] = value;
    setAnswers(updated);
  };

  const handleSubmit = () => {
    if (answers.includes("")) {
      alert("Please answer all questions before submitting.");
      return;
    }

    const total = answers.reduce((acc, ans) => acc + scoreMapping[ans], 0);
    const max = questions.length * 4;
    const percent = (total / max) * 100;

    let level = "";
    if (percent < 33) level = "Low FOMO tendencies";
    else if (percent < 66) level = "Moderate FOMO tendencies";
    else level = "High FOMO tendencies";

    setScore(total);
    setResult(level);
    setSubmitted(true);

    const profile = JSON.parse(localStorage.getItem("user_profile")) || {};
    profile["FOMO Score"] = total;
    profile["FOMO Level"] = level;
    localStorage.setItem("user_profile", JSON.stringify(profile));

    const remaining = JSON.parse(localStorage.getItem("remaining_issues")) || [];
    const updatedRemaining = remaining.filter((item) => item !== "Social Media FOMO");
    localStorage.setItem("remaining_issues", JSON.stringify(updatedRemaining));

    setTimeout(() => {
      if (updatedRemaining.length > 0) {
        //const next = updatedRemaining[0].toLowerCase().replace(/\s+/g, "-");
        let next = updatedRemaining[0].toLowerCase();
        if (next.includes("fomo")) next = "fomo";
        navigate(`/assessment-${next}`);
      } else {
        navigate("/chat");
      }
    }, 4000);
  };

  return (
    <Card className="max-w-xl mx-auto mt-10 p-6">
      {!submitted ? (
        <>
          <h2 className="text-xl font-semibold mb-4">📱 FOMO Assessment</h2>
          <p className="mb-6">Please indicate how much the following statements apply to you:</p>
          {questions.map((q, i) => (
            <div key={i} className="mb-4">
              <p className="mb-2">{q}</p>
              <select
                className="w-full p-2 border rounded"
                value={answers[i]}
                onChange={(e) => handleChange(i, e.target.value)}
              >
                <option value="">Select</option>
                {options.map((opt, idx) => (
                  <option key={idx} value={opt}>{opt}</option>
                ))}
              </select>
            </div>
          ))}
          <Button onClick={handleSubmit}>Submit</Button>
        </>
      ) : (
        <>
          <h2 className="text-xl font-semibold mb-4">Assessment Complete</h2>
          <p>Your score: {score} / {questions.length * 4}</p>
          <p>Result: <strong>{result}</strong></p>
          <p className="text-sm text-gray-500 mt-2">Redirecting shortly...</p>
        </>
      )}
    </Card>
  );
};

export default AssessmentFOMO;
