"use client";
import React, { use, useState } from "react";
import { useRouter } from "next/navigation";
import AuthFooterLinks from "./AuthFooterLinks";

export default function LoginForm() {
    const router = useRouter ();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState ("");
    const [error, setError] = useState ("");

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch (`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password}),
            });
            const data = await res.json();
            if (res.ok && data.success) {
                router.push (`/auth/verify?email=${encodeURIComponent(email)}`);
            } else {
                setError(data.detail || data.error || "Login failed");
            }
        } catch (err) {
            setError("Network Error");
        }
    };

    return (
        <>
            <form onSubmit={handleLogin} className="space-y-4 p-4 max-w-sm mx-auto">
                <h2 className="text-xl font-bold text-center">Login</h2>
                <input
                    type="email"
                    placeholder="Email"
                    className="w-full p-2 border rounded"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                {error && <p className="text-red-500 text-sm">{error}</p>}
                <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">
                    Submit
                </button>
            </form>
            <AuthFooterLinks type="login" />
        </>
    );
}