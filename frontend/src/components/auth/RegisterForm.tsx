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
    // useState("") returns an array: * led by useState
    // → ["", function to update the state]
    // Name: Array Destructuring

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.type]: e.target.value})
    }; // since form now enatils multiple value
    // we have to set form through destructuring, to do each one by one
    // handleChange knows which value to update through the TYPE attribute down below
    // using NAME attribute is preferred as type require case specific

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch (`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
                method: "POST",
                headers: { "Content-Type" : "application/json" },
                body: JSON.stringify(form), // the entire form here, with its key & data inside
            });

            const data = await res.json();
            if (res.ok && data.success) {
                router.push(`/auth/verify?email{encodeURIComponent(form.email)}`);
            } else { // push - render not reloading
                setError(data.detail || data.error || "Registration failed.");
            }
        } catch (err) {
            setError("Network error");
        } 
    };

    // so here is where we see everything in action, if u went through in descending order...
    // u should have a good grasp already
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