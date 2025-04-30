"use client"
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import AuthFooterLinks from "./AuthFooterLinks";

export default function ForgotPasswordForm() {
    const router = useRouter();
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setMessage("");

        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/forgot-password`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email }),
            });
        
            const data = await res.json();
            if (res.ok && data.success) {
                router.push(`/auth/reset?email=${encodeURIComponent(email)}`);
            } else {
                setError(data.detail || data.error || "Something Went Wrong.")
            }
        } catch {
            setError("Network error");
        }
    };

    return (
        <>
        <form onSubmit={handleSubmit} className="space-y-4 p-4 max-w-sm mx-auto">
            <h2 className="text-xl font-bold text-center">ForgotPassword</h2>
            <input
                type="email"
                placeholder="Enter your email"
                className="w-full p-2 border rounded"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded">
                Send OTP
            </button>    
        </form>
        <AuthFooterLinks type="forgot" />
        </>
    );
}