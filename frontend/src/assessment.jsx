import React, { useState } from "react";
import { Link } from "react-router-dom";

const anxietyGroup = [
  "Not at all",

  "Several days",
  "More than half the days",

  "Nearly every day",
];


const depressionGroup = [  "Not at all",

  "Several days",
  "More than half the days",

  "Nearly every day"];


const stressGroup = ["Never",

"Almost never",

"Sometimes",

"Fairly often",

"Very often"];


const adhdGroup = [
  "Never",

"Rarely",

"Sometimes",

"Often",

"Very often"
];





const privacyConsent = [
  "I consent to the storage and processing of my data as described in the privacy policy. I understand that MindfulChat is not a replacement for professional mental health services.",
];

// Step 1 Component (Example - customize with your fields)
const Step1 = ({ form, handleChange }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
      Feeling nervous, anxious, or on edge


      </label>
      <div className="space-y-2">
        {anxietyGroup.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="anxietyGroup"
              value={group}
              checked={form.anxietyGroup === group}
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

// Step 2 Component (Example - customize with your fields)
const Step2 = ({ form, handleChange }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
      Little interest or pleasure in doing things

      </label>
      <div className="space-y-2">
        {depressionGroup.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="depressionGroup"
              value={group}
              checked={form.depressionGroup === group}
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
      Been upset because of something that happened unexpectedly?

      </label>
      <div className="space-y-2">
        {stressGroup.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="stressGroup"
              value={group}
              checked={form.stressGroup === group}
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



// Step 4 Component (Example - customize with your fields)
const Step4 = ({ form, handleChange }) => {
  return (
    <>
      <label className="block mb-2 text-sm font-medium text-gray-900">
      How often do you have difficulty getting things in order when you have to do a task that requires organization?



      </label>
      <div className="space-y-2">
        {adhdGroup.map((group) => (
          <div className="flex items-center" key={group}>
            <input
              type="radio"
              id={group}
              name="adhdGroup"
              value={group}
              checked={form.adhdGroup === group}
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
const Assessment = ({setAssessEval}) => {
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({
    anxietyGroup: "",
    depressionGroup: "",
    stressGroup: "",
    adhdGroup: "",
  });

  const steps = [
    "Anxiety Assessment",
    "Depression Assessment",
    "Stress Assessment",
    "ADHD Assessment",
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };


  const submitForm = async () => {
    const response = await fetch("http://localhost:8000/store/assessment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form), // Assuming 'form' is the data you want to send
      });
   
    const assessment_json = await response.json()
    setAssessEval(assessment_json.reply)
    
    
  };





  


  const handleSubmit = (e) => {
    e.preventDefault();
    // Submit data to your API here
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

        <div className="mb-6 text-black text-center font-bold bg-green-50 p-2">
          <h1> Step {step} of {steps.length}: {steps[step - 1]}</h1>
          <h1 className="text-sm font-medium"> Over the past 2 weeks, how often have you been bothered by the following problems?</h1>
        </div>

      

        {step === 1 && <Step1 form={form} handleChange={handleChange} />}
        {step === 2 && <Step2 form={form} handleChange={handleChange} />}
        {step === 3 && <Step3 form={form} handleChange={handleChange} />}
        {step === 4 && <Step4 form={form} handleChange={handleChange} />}
        

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
          ) : form.adhdGroup.length == 0 ? (
            <button
              type="button"
              className="ml-auto text-white bg-gray-300 cursor-not-allowed font-medium rounded-lg text-sm px-5 py-2.5"
             
            >
              Submit
            </button>
          ) : (
            <Link to="/chat">
              <button
                type="button"
                onClick={() => submitForm()}
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

export default Assessment;
