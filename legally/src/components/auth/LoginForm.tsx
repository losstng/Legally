"use client";
import React, { use, useState } from "react";
import { useRouter } from "next/navigation";
import AuthFooterLinks from "./AuthFooterLinks";
import { useAuth } from "@/utils/authcontext";
import { loginUser } from "@/utils/api";

interface LoginResponse {
    success: boolean;
    detail?: string;
    error?: string;
  }

export default function LoginForm() {
    const router = useRouter (); // to push = render without reload
    const [email, setEmail] = useState(""); // initially empty
    const [password, setPassword] = useState ("");
    const [error, setError] = useState ("");
    // useState("") returns an array:
    // → ["", function to update the state]
    // Name: Array Destructuring
    const { setPrefillEmail } = useAuth();
    
    
    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault(); // preventing html automatic response of reloading
        setError("");

        try {
            const { success, data } = await loginUser(email, password);
            // fetch is a natural function built in the engine
            // used to send one of 4 method in POST, GET, PUT, DELETE
            // headers are letter-specific due to it being JSON and latter parsed for server
            // these can include tokens, type, the response model, and cookies
            // the order of these don't matter

        
            if (success) { 
        // res.ok is success on the HTTP level, while success is for the backend level
                router.push (`/auth/verify?email=${encodeURIComponent(email)}`);
                setPrefillEmail(email);
            } else { // push - render that page—but don’t reload the browser
                setError(data?.detail || data?.error || "Login failed");
            }
        } catch {
            setError("Network Error");
        } //If either the HTTP layer (res.ok) or app logic (data.success) fails, the else block handles it; 
        // if the entire request fails, catch takes over.
    }; // (err) is here ...
    // because catch(...) always receives the error that was thrown inside the try block.
    // if we skip it like in ForgotPassWord, we wouldn't be able to LOG IT 

    // also take note of the "on...={handle...}"" due to its importance on said action
    // also the "set" as it will be used in order update the value for handle... to send
    return (
  <>
    <form
      onSubmit={handleLogin}
      className="space-y-6 p-6 bg-white rounded-md shadow-sm w-full max-w-sm mx-auto"
    >
      <h2 className="text-2xl font-semibold text-center text-blue-700">Login</h2>

      <div className="space-y-4 mx-auto w-[40%]">
        <input
          type="email"
          placeholder="Email"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        {error && (
          <p className="text-sm text-red-600 text-center">{error}</p>
        )}

        <button
          type="submit"
          className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded transition duration-200"
        >
          Submit
        </button>
      </div>
    </form>

    <div className="mt-6">
      <AuthFooterLinks type="login" />
    </div>
  </>
);
}