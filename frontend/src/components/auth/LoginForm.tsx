"use client";
import React, { use, useState } from "react";
import { useRouter } from "next/navigation";
import AuthFooterLinks from "./AuthFooterLinks";
import { useAuth } from "@/utils/authcontext";

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
            const res = await fetch (`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password}),
            });
            // fetch is a natural function built in the engine
            // used to send one of 4 method in POST, GET, PUT, DELETE
            // headers are letter-specific due to it being JSON and latter parsed for server
            // these can include tokens, type, the response model, and cookies
            // the order of these don't matter

            const data = await res.json();
            if (res.ok && data.success) { 
        // res.ok is success on the HTTP level, while success is for the backend level
                router.push (`/auth/verify?email=${encodeURIComponent(email)}`);
                setPrefillEmail(email);
            } else { // push - render that page—but don’t reload the browser
                setError(data.detail || data.error || "Login failed");
            }
        } catch (err) {
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
        {/* onSubmit is a DOM event that’s tied specifically to the <form> element. */}
        {/* Inside a <form>, when a button of type "submit" is clicked, the browser knows to trigger the form’s onSubmit event. */}
            <form onSubmit={handleLogin} className="space-y-4 p-4 max-w-sm mx-auto">
                <h2 className="text-xl font-bold text-center">Login</h2>
                <input
                    type="email"
                    placeholder="Email"
                    className="w-full p-2 border rounded"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                /> {/* as we are using React, an interface manipulating DOM, 
                    the object might not always be as synchronized so e or what ever object we declare will be the action object */}
                {error && <p className="text-red-500 text-sm">{error}</p>}
                {/* same logic of is left occurs then right occurs */}
                <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">
                    Submit
                </button>
            </form>
            <AuthFooterLinks type="login" /> {/* take note of the type here */}
        </>
    );
}