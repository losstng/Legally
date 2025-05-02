import React from "react";

export default function AuthlAyout({ children }: { children: React.ReactNode}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md bg-white rounded shadow-md p-6">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-blue-700">Legally</h1>
          <p className="text-sm text-gray-500">Secure your legal journey</p>
        </div>
        {children}
      </div>
    </div>
  );
}
// the children here are below, essentially what will be passed in the main page.tsx