import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "./ui/Card";
import { Button } from "./ui/Button";

const Profile = () => {
  const [profile, setProfile] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedProfile = localStorage.getItem("user_profile");
    if (storedProfile) {
      setProfile(JSON.parse(storedProfile));
    }
  }, []);

  const handleNext = () => {
    navigate("/assessment-selection");
  };

  if (!profile) {
    return <p className="text-center mt-10">No profile found. Please fill the form first.</p>;
  }

  return (
    <Card className="max-w-xl mx-auto mt-10 p-6 rounded-lg shadow-md bg-white">
      <h2 className="text-2xl font-semibold mb-6 text-teal-800">Your Profile</h2>

      <div className="grid grid-cols-2 gap-x-6 gap-y-3 text-sm">
        <div>
          <p className="text-gray-500">Name</p>
          <p className="font-medium">{profile.name || "-"}</p>
        </div>
        <div>
          <p className="text-gray-500">Age</p>
          <p className="font-medium">{profile.age || "-"}</p>
        </div>
        <div>
          <p className="text-gray-500">Gender</p>
          <p className="font-medium">{profile.gender || "-"}</p>
        </div>
        <div>
          <p className="text-gray-500">Financial Status</p>
          <p className="font-medium">{profile.financialStatus || "-"}</p>
        </div>
        <div>
          <p className="text-gray-500">Education</p>
          <p className="font-medium">{profile.education || "-"}</p>
        </div>
        <div>
          <p className="text-gray-500">Generation</p>
          <p className="font-medium">{profile.generation || "-"}</p>
        </div>
        <div className="col-span-2">
          <p className="text-gray-500">Mental Health State</p>
          <p className="font-medium">{profile["Current Mental Health State"] || "-"}</p>
        </div>
        {profile["Mental Health Issues"]?.length > 0 && (
          <div className="col-span-2">
            <p className="text-gray-500 mb-2">Mental Health Issues</p>
            <div className="flex flex-wrap gap-2">
              {profile["Mental Health Issues"].map((issue, i) => (
                <span
                  key={i}
                  className="bg-teal-100 text-teal-700 px-3 py-1 rounded-full text-sm font-medium"
                >
                  {issue}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="flex justify-between mt-6">
        <Button variant="outline" onClick={() => navigate("/privacy-consent")}>
          Edit Profile
        </Button>
        <Button onClick={handleNext}>Continue to Assessment</Button>
      </div>
    </Card>
  );
};

export default Profile;
