import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

const questions = [
  "Feeling nervous, anxious, or on edge?",
  "Not being able to stop or control worrying?",
  "Worrying too much about different things?",
  "Trouble relaxing?",
  "Being so restless that it is hard to sit still?",
  "Becoming easily annoyed or irritable?",
  "Feeling afraid as if something awful might happen?"
];

const options = [
  "Not at all",
  "Several days",
  "More than half the days",
  "Nearly every day"
];

const scoreMapping = {
  "Not at all": 0,
  "Several days": 1,
  "More than half the days": 2,
  "Nearly every day": 3
};

const AssessmentAnxiety = () => {
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

    let result = "";
    if (total <= 5) result = "Minimal anxiety";
    else if (total <= 10) result = "Mild anxiety";
    else if (total <= 15) result = "Moderate anxiety";
    else result = "Severe anxiety";

    setLevel(result);
    setSubmitted(true);

    const profile = JSON.parse(localStorage.getItem("user_profile")) || {};
    profile["Anxiety Score"] = total;
    profile["Anxiety Level"] = result;
    localStorage.setItem("user_profile", JSON.stringify(profile));

    const remaining = JSON.parse(localStorage.getItem("remaining_issues")) || [];
    const updatedRemaining = remaining.filter((item) => item !== "Anxiety");
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
          <h2 className="text-xl font-semibold mb-4">🌩️ Anxiety Assessment (GAD-7)</h2>
          <p className="mb-6">Over the last 2 weeks, how often have you been bothered by the following problems:</p>
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
          <p>Your score: {score} / {questions.length * 3}</p>
          <p>Result: <strong>{level}</strong></p>
          <p className="text-sm text-gray-500 mt-2">Redirecting...</p>
        </>
      )}
    </Card>
  );
};

export default AssessmentAnxiety;
