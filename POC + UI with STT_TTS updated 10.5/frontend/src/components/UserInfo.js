import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";
import Input from "./ui/Input";
import Label from "./ui/Label";

const UserInfo = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    financialStatus: "",
    education: "",
    generation: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleNext = () => {
    if (!form.name) {
      alert("Please enter your name");
      return;
    }
    localStorage.setItem("user_profile", JSON.stringify(form));
    navigate("/mental-health");
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-blue-50 to-teal-100 px-4">
      <Card className="w-full max-w-2xl p-8 shadow-lg rounded-xl bg-white">
        <h2 className="text-2xl font-bold mb-1 text-center text-teal-700">User Information</h2>
        <p className="text-sm text-gray-500 text-center mb-6">Step 1 of 3: Personal Information</p>

        <div className="w-full bg-gray-200 rounded-full h-2.5 mb-6">
          <div className="bg-teal-500 h-2.5 rounded-full" style={{ width: "30%" }}></div>
        </div>

        <div className="mb-4">
          <Label htmlFor="name">Name / Nickname (can be anonymous)</Label>
          <Input
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="How would you like to be called?"
          />
        </div>

        <div className="mb-4">
          <Label htmlFor="age">Age</Label>
          <select name="age" className="w-full p-2 border rounded" onChange={handleChange}>
            <option value="">Select your age group</option>
            <option value="Under 18">Under 18</option>
            <option value="18-24">18-24</option>
            <option value="25-34">25-34</option>
            <option value="35-44">35-44</option>
            <option value="45+">45+</option>
          </select>
        </div>

        <div className="mb-4">
          <Label htmlFor="gender">Gender (optional)</Label>
          <div className="flex flex-col gap-2 mt-2">
            {['Male', 'Female', 'Non-binary', 'Prefer not to say'].map((option) => (
              <label key={option} className="flex items-center gap-2">
                <input
                  type="radio"
                  name="gender"
                  value={option}
                  checked={form.gender === option}
                  onChange={handleChange}
                />
                {option}
              </label>
            ))}
          </div>
        </div>

        <div className="mb-4">
          <Label htmlFor="financialStatus">Financial Status</Label>
          <select
            name="financialStatus"
            className="w-full p-2 border rounded"
            onChange={handleChange}
          >
            <option value="">Select your financial status</option>
            <option value="Student">Student</option>
            <option value="Employed">Employed</option>
            <option value="Self-employed">Self-employed</option>
            <option value="Unemployed">Unemployed</option>
            <option value="Retired">Retired</option>
            <option value="Prefer not to say">Prefer not to say</option>
          </select>
        </div>

        <div className="mb-4">
          <Label htmlFor="education">Education</Label>
          <select name="education" className="w-full p-2 border rounded" onChange={handleChange}>
            <option value="">Select your education level</option>
            <option value="High school">High school</option>
            <option value="Some college">Some college</option>
            <option value="Bachelor's degree">Bachelor's degree</option>
            <option value="Master's degree">Master's degree</option>
            <option value="Doctorate">Doctorate</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="mb-6">
          <Label htmlFor="generation">Generation</Label>
          <select name="generation" className="w-full p-2 border rounded" onChange={handleChange}>
            <option value="">Select your generation</option>
            <option value="Gen Z (1997-2012)">Gen Z (1997-2012)</option>
            <option value="Millennial (1981-1996)">Millennial (1981-1996)</option>
            <option value="Gen X (1965-1980)">Gen X (1965-1980)</option>
            <option value="Baby Boomer (1946-1964)">Baby Boomer (1946-1964)</option>
            <option value="Other">Other</option>
          </select>
        </div>

        <div className="flex justify-end">
          <Button onClick={handleNext} className="px-6 py-2 text-white bg-teal-600 hover:bg-teal-700">
            Next
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default UserInfo;
