"use client";
import React, { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { verifyOTP, deleteUser, confirmPasswordChange } from "@/utils/api";

export default function VerifyOTPForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const email = searchParams.get("email") || "";
  const action = searchParams.get("action"); // "delete" | "change_password"
  const newPassword = searchParams.get("new_password");

  const [otp, setOtp] = useState("");
  const [error, setError] = useState("");

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const { success, data } = await verifyOTP(email, otp);
      if (!success) {
        setError(data?.detail || data?.error || "Invalid OTP");
        return;
      }

      const token = data.data.refresh_token;
      localStorage.setItem("token", token);

      if (action === "delete") {
        await deleteUser(token);
        localStorage.removeItem("token");
        router.push("/auth/login");
      } else if (action === "change_password" && newPassword) {
        await confirmPasswordChange(token, newPassword);
        router.push("/");
      } else {
        router.push("/");
      }
    } catch {
      setError("Network error");
    }
  };


  return (
  <form
    onSubmit={handleVerify}
    className="space-y-6 p-6 bg-white rounded-md shadow-sm w-full max-w-sm mx-auto"
  >
    <h2 className="text-2xl font-semibold text-center text-blue-700">
      Verify OTP
    </h2>

    <div className="space-y-4 mx-auto w-[40%]">
      <input
        type="text"
        placeholder="Enter OTP"
        className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        required
      />

      {error && (
        <p className="text-sm text-red-600 text-center">{error}</p>
      )}

      <button
        type="submit"
        className="w-full py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded transition duration-200"
      >
        Verify
      </button>

      <Link
        href="/auth/login"
        className="block text-center text-sm text-blue-600 hover:underline mt-2"
      >
        Back to Login
      </Link>
    </div>
  </form>
);
}