import React, { useState } from "react";
import {Link} from "react-router-dom"
const ageGroups = ["Under 18", "18-24", "25-34", "35-44", "45+"];

const genders = ["Male", "Female", "Non-binary", "Prefer not to say"];

const interactionStyles = ["Formal", "Informal"];

const mentalAreas = [
  "Anxiety",
  "Depression",
  "Stress",
  "Attention-Deficit/Hyperactivity Disorder (ADHD)",
];

const privacyConsent = [
  "I consent to the storage and processing of my data as described in the privacy policy. I understand that MindfulChat is not a replacement for professional mental health services.",
];

// Step 1 Component
const Step1 = ({ form, setForm }) => (
  <>
    <h2 className="text-2xl font-bold mb-2 text-gray-800">User Onboarding</h2>
    <div className="mb-5">
      <label
        htmlFor="name"
        className="block mb-2 text-sm font-medium text-gray-900"
      >
        Name / Nickname (can be anonymous)
      </label>
      <input
        type="text"
        name="name"
        id="name"
        placeholder="How would you like to be called?"
        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2.5"
        value={form.name}
        onChange={(e) => setForm({ ...form, name: e.target.value })}
        required
      />
    </div>
    {/* Add other Step 1 fields from previous example */}
  </>
);

// Step 2 Component (Example - customize with your fields)
const Step2 = ({ form, handleChange }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
        Age Group
      </label>
      <div className="space-y-2">
        {ageGroups.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="ageGroup"
              value={group}
              checked={form.ageGroup === group}
              onChange={handleChange}
              className="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 focus:ring-green-500"
              required
            />
            <label htmlFor={group} className="ml-2 text-sm text-gray-900">
              {group}
            </label>
          </div>
        ))}
      </div>
    </>
  );
};

// Step 3 Component (Example - customize with your fields)
const Step3 = ({ form, handleChange }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
        Gender
      </label>
      <div className="space-y-2">
        {genders.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="gender"
              value={group}
              checked={form.gender === group}
              onChange={handleChange}
              className="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 focus:ring-green-500"
              required
            />
            <label htmlFor={group} className="ml-2 text-sm text-gray-900">
              {group}
            </label>
          </div>
        ))}
      </div>
    </>
  );
};

const Step4 = ({ form, handleChange }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
        Preferred Interaction Style
      </label>
      <div className="space-y-2">
        {interactionStyles.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="interactionStyle"
              value={group}
              checked={form.interactionStyle === group}
              onChange={handleChange}
              className="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 focus:ring-green-500"
              required
            />
            <label htmlFor={group} className="ml-2 text-sm text-gray-900">
              {group}
            </label>
          </div>
        ))}
      </div>
    </>
  );
};

const Step5 = ({ form, handleChangeCheckbox }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
        Area of Concern (select all that apply)
      </label>
      <div className="space-y-2">
        {mentalAreas.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="checkbox"
              id={group}
              name="mentalAreas"
              value={group}
              checked={form.mentalAreas.includes(group)}
              onChange={handleChangeCheckbox}
              className="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 focus:ring-green-500"
            />
            <label htmlFor={group} className="ml-2 text-sm text-gray-900">
              {group}
            </label>
          </div>
        ))}
      </div>
    </>
  );
};

const Step6 = ({ form, handleChangeCheckbox }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
        Area of Concern (select all that apply)
      </label>
      <div className="text-black p-3 bg-green-100 text-center ">
        Privacy & Data Usage GreenLife values your privacy. Your conversations
        are encrypted and stored securely. We use anonymized data to improve our
        service and provide better support. You can request deletion of your
        data at any time.
      </div>
      <div className="space-y-2 pt-3">
        {privacyConsent.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="checkbox"
              id={group}
              name="privacyConsent"
              value={group}
              checked={form.privacyConsent.includes(group)}
              onChange={handleChangeCheckbox}
              className="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 focus:ring-green-500"
            />
            <label htmlFor={group} className="ml-2 text-sm text-gray-900">
              {group}
            </label>
          </div>
        ))}
      </div>
    </>
  );
};

// Stepper Component
const Stepper = ({ steps, currentStep }) => (
  <div className="flex items-center justify-center mb-8">
    {steps.map((step, index) => (
      <div key={step} className="flex items-center">
        <div
          className={`w-8 h-8 rounded-full flex items-center justify-center ${
            index + 1 <= currentStep
              ? "bg-green-600 text-white"
              : "bg-gray-200 text-gray-500"
          }`}
        >
          {index + 1}
        </div>
        {index < steps.length - 1 && (
          <div
            className={`h-1 w-16 ${index + 1 < currentStep ? "bg-green-600" : "bg-gray-200"}`}
          />
        )}
      </div>
    ))}
  </div>
);

// Main Wizard Component
const Onboarding = () => {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    name: "",
    ageGroup: "",
    gender: "",
    interactionStyle: "",
    mentalAreas: [],
    privacyConsent: [],
  });

  const steps = [
    "Basic Info",
    "Age Group",
    "Gender",
    "Interaction Style",
    "Areas of Concern",
    "Privacy & Consent",
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleChangeCheckbox = (e) => {
    const { name, value, checked } = e.target;

    if (name === "mentalAreas" || name === "privacyConsent") {
      setForm((prev) => ({
        ...prev,
        [name]: checked
          ? [...prev[name], value] // add to array
          : prev[name].filter((g) => g !== value), // remove from array
      }));
    } else {
      setForm((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async () => {
    // Submit data to your API here
    const user_info_data = await fetch ("http://localhost:8000/store/onboarding", {
      "method": "POST",
      "headers": {
        "Content-Type": "application/json",
      },
      "body": JSON.stringify(form)
    }) 
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <form
        className="bg-white p-8 rounded shadow-md w-full max-w-lg"
        onSubmit={handleSubmit}
        onKeyDown={(e) => {
          // Prevent Enter from submitting the form except on the last step
          if (e.key === "Enter" && step < steps.length) {
            e.preventDefault();
          }
        }}
      >
        <Stepper steps={steps} currentStep={step} />

        <p className="mb-6 text-black text-center font-bold bg-green-50 p-2">
          Step {step} of {steps.length}: {steps[step - 1]}
        </p>

        {step === 1 && <Step1 form={form} setForm={setForm} />}
        {step === 2 && <Step2 form={form} handleChange={handleChange} />}
        {step === 3 && <Step3 form={form} handleChange={handleChange} />}
        {step === 4 && <Step4 form={form} handleChange={handleChange} />}
        {step === 5 && (
          <Step5 form={form} handleChangeCheckbox={handleChangeCheckbox} />
        )}
        {step === 6 && (
          <Step6 form={form} handleChangeCheckbox={handleChangeCheckbox} />
        )}

        <div className="flex justify-between mt-8">
          {step > 1 && (
            <button
              type="button"
              onClick={() => setStep(step - 1)}
              className="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 font-medium rounded-lg text-sm px-5 py-2.5"
            >
              Back
            </button>
          )}

          {step < steps.length ? (
            <button
              type="button"
              onClick={() => setStep(step + 1)}
              className="ml-auto text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5"
            >
              Next
            </button>
          ) : form.privacyConsent.length == 0 ? (
            <button
              type="button"
              className="ml-auto text-white bg-gray-300 cursor-not-allowed font-medium rounded-lg text-sm px-5 py-2.5"
              disabled={step !== 6} // Disable submit until Step 5
            >
              Submit
            </button>
          ) : (
            <Link to="/assessmentModal">
              <button
                type="button"
                onClick={() => {handleSubmit()}}
                className="ml-auto cursor-pointer text-white bg-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5"
              >
                Submit
              </button>
            </Link>
          )}
        </div>
      </form>
    </div>
  );
};

export default Onboarding;
