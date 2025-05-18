// src/components/ui/Label.js
import React from "react";

const Label = ({ children, htmlFor, className = "", ...props }) => {
  return (
    <label
      htmlFor={htmlFor}
      className={`block mb-1 font-medium text-gray-700 ${className}`}
      {...props}
    >
      {children}
    </label>
  );
};

export default Label;
