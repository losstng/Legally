"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import AuthFooterLinks from "./AuthFooterLinks";
import { registerUser } from "@/utils/api";

export default function RegisterForm() {
  const router = useRouter();
  const [form, setForm] = useState({
    name: "",
    age: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
  
    const payload = {
      ...form,
      age: Number(form.age),
    };
  
    try {
      const { success, data } = await registerUser(payload);
  
      if (success) {
        router.push(`/auth/verify?email=${encodeURIComponent(form.email)}&action=register`);
      } else {
        if (typeof data.detail === "string") {
          setError(data.detail);
        } else if (Array.isArray(data.detail)) {
          setError(data.detail.map((d: any) => d.msg).join(", "));
        } else {
          setError("Registration failed.");
        }
      }
    } catch {
      setError("Network error.");
    }
  };

  return (
  <>
    <form
      onSubmit={handleRegister}
      className="space-y-6 p-6 bg-white rounded-md shadow-sm w-full max-w-sm mx-auto"
    >
      <h2 className="text-2xl font-semibold text-center text-blue-700">Register</h2>

      <div className="space-y-4 mx-auto w-[40%]">
        <input
          name="name"
          type="text"
          placeholder="Full Name"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          name="age"
          type="number"
          placeholder="Age"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={form.age}
          onChange={handleChange}
          required
        />

        <input
          name="email"
          type="email"
          placeholder="Email"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={form.email}
          onChange={handleChange}
          required
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={form.password}
          onChange={handleChange}
          required
        />

        {error && (
          <p className="text-sm text-red-600 text-center">
            {typeof error === "string" ? error : JSON.stringify(error)}
          </p>
        )}

        <button
          type="submit"
          className="w-full py-2 bg-blue-700 hover:bg-blue-800 text-white font-medium rounded transition duration-200"
        >
          Register
        </button>
      </div>
    </form>

    <div className="mt-6">
      <AuthFooterLinks type="register" />
    </div>
  </>
);
}