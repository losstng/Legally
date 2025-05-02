"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/utils/authcontext";

export default function ProtectedRoute({ children}: { children: React.ReactNode}) {
    const { user } = useAuth();
    // pulls the user from global context
    const router = useRouter();
    // ability to control navigation in react & backend

    useEffect(() => { // effect when user or router changes
        if (!user) { 
            router.replace("/auth/login"); 
        } // redirect to log in in any unsuccessful cases
    }, [user, router]); // Only re-run the useEffect callback if either user or router changes.
    // above is dependecy array - watches any changes to 2 prop to re-execute
    if (!user) return null; // if no user is found, halts rendering

    return <>{children}</> // if user is found then return children
}