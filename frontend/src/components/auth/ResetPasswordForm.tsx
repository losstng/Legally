"use client";
import React, { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

export default function ResetPasswordForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const email = searchParams.get("email") || "";

    const [otp, setOtp] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [error, setError] = useState("");

    const handleReset = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/reset-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, otp, newPassword: newPassword }),
            });

            const data = await res.json();
            if (res.ok && data.success) {
                router.push("/auth/login");
            } else {
                setError(data.detail || data.error || "Reset failed");
            }
        } catch {
            setError("Network error");
        }
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
          />
          <input
            type="password"
            placeholder="New Password"
            className="w-full p-2 border rounded"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
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