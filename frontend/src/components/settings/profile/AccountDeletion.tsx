"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
export default function AccountDeletion() {
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");
    const router = useRouter();

    const handleRequestDelete = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        
        try {
            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/request-delete`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ email }),
            });
      
            const data = await res.json();
            if (res.ok && data.success) {
              router.push(`/auth/verify?email=${encodeURIComponent(email)}&action=delete`);
            } else {
              setError(data.detail || data.error || "Failed to initiate deletion.");
            }
          } catch {
            setError("Network error.");
          }
        };
      
        return (
          <form onSubmit={handleRequestDelete} className="max-w-md mx-auto mt-10 p-6 border rounded bg-white shadow">
            <h2 className="text-lg font-bold mb-4">Delete Your Account</h2>
            <p className="mb-4 text-sm text-gray-600">You’ll receive an OTP to confirm deletion.</p>
            <input
              type="email"
              className="w-full p-2 border rounded mb-4"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
            <button type="submit" className="bg-red-600 text-white py-2 px-4 rounded hover:bg-red-700">
              Request Deletion
            </button>
          </form>
        );
    }
