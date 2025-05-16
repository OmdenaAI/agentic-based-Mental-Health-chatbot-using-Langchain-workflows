import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

const questions = [
  "Been upset because of something that happened unexpectedly?",
  "Felt that you were unable to control the important things in your life?",
  "Felt nervous and stressed?",
  "Felt confident about your ability to handle your personal problems?",
  "Felt that things were going your way?",
];

const options = ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"];

const scoreMapping = {
  "Never": 0,
  "Almost never": 1,
  "Sometimes": 2,
  "Fairly often": 3,
  "Very often": 4,
};

const AssessmentStress = () => {
  const navigate = useNavigate();
  const [answers, setAnswers] = useState(Array(questions.length).fill(""));
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [level, setLevel] = useState("");

  const handleChange = (index, value) => {
    const updated = [...answers];
    updated[index] = value;
    setAnswers(updated);
  };

  const handleSubmit = () => {
    if (answers.includes("")) {
      alert("Please answer all questions.");
      return;
    }

    const total = answers.reduce((sum, ans) => sum + scoreMapping[ans], 0);
    setScore(total);

    const maxScore = questions.length * 4;
    const percentage = (total / maxScore) * 100;

    let stressLevel = "";
    if (percentage < 33) stressLevel = "Low stress";
    else if (percentage < 66) stressLevel = "Moderate stress";
    else stressLevel = "High stress";

    setLevel(stressLevel);
    setSubmitted(true);

    const profile = JSON.parse(localStorage.getItem("user_profile")) || {};
    profile["Stress Score"] = total;
    profile["Stress Level"] = stressLevel;
    localStorage.setItem("user_profile", JSON.stringify(profile));

    const remaining = JSON.parse(localStorage.getItem("remaining_issues")) || [];
    const updatedRemaining = remaining.filter((item) => item !== "Stress");
    localStorage.setItem("remaining_issues", JSON.stringify(updatedRemaining));

    setTimeout(() => {
      if (updatedRemaining.length > 0) {
        //const next = updatedRemaining[0].toLowerCase();
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
          <h2 className="text-xl font-semibold mb-4">💥 Stress Assessment (PSS-5)</h2>
          <p className="mb-6">Please indicate how often you have felt or thought a certain way during the last month:</p>
          {questions.map((q, i) => (
            <div key={i} className="mb-4">
              <p className="mb-2 font-medium">{q}</p>
              <select
                className="w-full p-2 border rounded"
                value={answers[i]}
                onChange={(e) => handleChange(i, e.target.value)}
              >
                <option value="">Select</option>
                {options.map((opt, j) => (
                  <option key={j} value={opt}>{opt}</option>
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
          <p>Result: <strong>{level}</strong></p>
          <p className="text-sm text-gray-500 mt-2">Redirecting to next step...</p>
        </>
      )}
    </Card>
  );
};

export default AssessmentStress;
