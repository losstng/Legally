"use client"
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import AuthFooterLinks from "./AuthFooterLinks";
import { requestPasswordReset } from "@/utils/api";

export default function ForgotPasswordForm() {
    const router = useRouter(); // to push = render without reload
    const [email, setEmail] = useState(""); // initially empty
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    // useState("") returns an array:
    // → ["", function to update the state]
    // Name: Array Destructuring
    
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault(); // preventing html automatic response of reloading
        setError(""); // first these would blank
        setMessage("");

        try {
            const { success, data } = await requestPasswordReset(email);
            if (success) {
              router.push(`/auth/reset?email=${encodeURIComponent(email)}`);
            } else {
              setError(data.detail || data.error || "Something Went Wrong.");
            }
          } catch {
            setError("Network error");
         //If either the HTTP layer (res.ok) or app logic (data.success) fails, the else block handles it; 
          // if the entire request fails, catch takes over.
          // skipping (err) prop here means we wouldn't be able to log it
          }
        }

    // Since each frontend component handles one clear interaction, 
    // it makes sense to mirror this clarity in the backend architecture
    // so the endpoints align naturally with the UI’s flow.


    // also take note of the "on...={handle...}"" due to its importance on said action
    // also the "set" as it will be used in order update the value for handle... to send
    return (
  <>
    <form
      onSubmit={handleSubmit}
      className="space-y-6 p-6 bg-white rounded-md shadow-sm w-full max-w-sm mx-auto"
    >
      <h2 className="text-2xl font-semibold text-center text-blue-700">
        Forgot Password
      </h2>

      <div className="space-y-4 mx-auto w-[40%]">
        <input
          type="email"
          placeholder="Enter your email"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        {error && (
          <p className="text-sm text-red-600 text-center">{error}</p>
        )}

        <button
          type="submit"
          className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded transition duration-200"
        >
          Send OTP
        </button>
      </div>
    </form>

    <div className="mt-6">
      <AuthFooterLinks type="forgot" />
    </div>
  </>
);
}