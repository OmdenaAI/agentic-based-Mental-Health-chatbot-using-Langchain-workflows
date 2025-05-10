// src/components/ui/Button.js
import React from "react";
import classNames from "classnames";

export const Button = ({ children, className, ...props }) => {
  return (
    <button
      className={classNames(
        "bg-blue-600 text-white px-4 py-2 rounded-xl hover:bg-blue-700 transition",
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
