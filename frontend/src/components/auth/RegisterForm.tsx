"use client"
import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { EXPORT_DETAIL } from "next/dist/shared/lib/constants";
import AuthFooterLinks from "./AuthFooterLinks";

export default function RegisterForm () {
    const router = useRouter();
    const [form, setForm] = useState({
        name: "",
        age: "",
        email: "",
        password: "",
    });
    const [error, setError] = useState("");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form})
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch (`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
                method: "POST",
                headers: { "Content-Type" : "application/json" },
                body: JSON.stringify(form),
            });

            const data = await res.json();
            if (res.ok && data.success) {
                router.push(`/auth/verify?email{encodeURIComponent(form.email)}`);
            } else {
                setError(data.detail || data.error || "Registration failed.");
        
            }
        } catch (err) {
            setError("Network error");
        }
    };

    return (
        <>    
        <form onSubmit={handleRegister} className="space-y-4 p-4 max-w-sm mx-auto">
            <h2 className="text-xl font-bold text-conter">Register</h2>
            <input name="name" type="text" placeholder="Full Name" className="w-full p-2 border rounded" required onChange={handleChange} />
            <input name="age" type="number" placeholder="Age" className="w-full p-2 border rounded" required onChange={handleChange} />
            <input name="email" type="email" placeholder="Email" className="w-full p-2 border rounded" required onChange={handleChange}/>
            <input name="password" type="password" placeholder="Password" className="w-full p-2 border rounded" required onChange={handleChange} />
            {error && <p className="text-red-500 text-sm">{error}</p>}
            <button type="submit" className="w-full bg-blue-700 text-white py-2 rounded">Register</button>
        </form>
        <AuthFooterLinks type="register"/>
        </>
    );
}