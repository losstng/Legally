"use client";
import React, { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { resetUserPassword } from "@/utils/api";

export default function ResetPasswordForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const email = searchParams.get("email") || "";
    // This hook (from Next.js’ app router) gives you access to the current URL’s query string.
    // Example URL: https://yoursite.com/auth/verify?email=abc@example.com
    // .get("email") retrieves the value of the email parameter from the URL.

    // useState("") returns an array:
    // → ["", function to update the state]
    // Name: Array Destructuring
    const [otp, setOtp] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [error, setError] = useState("");

    const handleReset = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
          const { success, data } = await resetUserPassword(email, otp, newPassword);
            
          if (success) {
                router.push("/auth/login");
            } else {
              setError(
                typeof data.detail === "string"
                  ? data.detail
                  : typeof data.error === "string"
                  ? data.error
                  : JSON.stringify(data.detail || data.error || "Reset failed")
              );
            }
        } catch {
            setError("Network error");
        } // no logging here
    };

    return (
        <form onSubmit={handleReset} className="space-y-4 p-4 max-w-sm mx-auto">
          <h2 className="text-xl font-bold text-center">Reset Password</h2>
          <input
            type="text"
            placeholder="OTP Code"
            className="w-full p-2 border rounded"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            required
          /> {/* the place for OTP */}
          <input
            type="password"
            placeholder="New Password"
            className="w-full p-2 border rounded"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />  {/* the place for password */}
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button type="submit" className="w-full bg-emerald-600 text-white py-2 rounded">
            Submit
          </button>
          <Link href="/auth/login" className="block text-center text-sm text-blue-600 hover:underline mt-4">
            Back to Login
          </Link>
        </form>
    );
}