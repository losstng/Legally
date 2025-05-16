import React from "react";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        {/* Header */}
        <header className="mb-10">
          <h1 className="text-5xl font-extrabold text-blue-700 leading-tight">
            Legally
          </h1>
          <p className="text-base text-gray-500 mt-2">
            Secure your legal journey
          </p>
        </header>

        {/* Form/Card Wrapper */}
        <div className="bg-white shadow-md rounded-md p-6 space-y-6">
          {children}
        </div>
      </div>
    </div>
  );
}