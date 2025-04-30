"use client";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/utils/authcontext";

export default function ProtectedRoute({ children}: { children: React.ReactNode}) {
    const { user } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!user) {
            router.replace("/auth/login");
        }
    }, [user, router]);

    if (!user) return null;

    return <>{children}</>
}