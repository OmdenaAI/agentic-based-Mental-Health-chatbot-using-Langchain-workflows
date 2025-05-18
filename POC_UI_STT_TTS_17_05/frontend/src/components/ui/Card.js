// src/ui/card.js
export function Card({ children, className = "", ...props }) {
    return (
      <div
        className={`rounded-2xl border shadow-sm p-4 bg-white ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
  