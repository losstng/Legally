"use client";
import React, { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

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
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, otp }),
      });

      const data = await res.json();
      if (res.ok && data.success) {
        const token = data.data.refresh_token;
        localStorage.setItem("token", token);

        if (action === "delete") {
          await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/delete-user`, {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });
          localStorage.removeItem("token");
          router.push("/auth/login");
        } else if (action === "change_password" && newPassword) {
          await fetch(`${process.env.NEXT_PUBLIC_API_URL}/settings/confirm-password-change`, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ new_password: newPassword }),
          });
          router.push("/settings/security");
        } else {
          router.push("/");
        }
      } else {
        setError(data.detail || data.error || "Invalid OTP");
      }
    } catch {
      setError("Network error");
    }
  };

  return (
    <form onSubmit={handleVerify} className="space-y-4 max-w-sm mx-auto">
      <h2 className="text-xl font-bold text-center">Verify OTP</h2>
      <input
        type="text"
        placeholder="Enter OTP"
        className="w-full p-2 border rounded"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        required
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <button type="submit" className="w-full bg-green-600 text-white py-2 rounded">
        Verify
      </button>
      <Link href="/auth/login" className="block text-center text-sm text-blue-600 hover:underline mt-4">
        Back to Login
      </Link>
    </form>
  );
}