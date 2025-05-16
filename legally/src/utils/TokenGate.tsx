"use client";
import React, { Children, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function TokenGate({ children }: { children: React.ReactNode }) {
    const router = useRouter();
    const [checking, setChecking] = useState(true);

    useEffect(() => {
        const token =localStorage.getItem("token");
        if (!token) {
            router.replace("/auth/login");
        } else {
            setChecking(false);
        }
    }, []);

    if (checking) return null;
    return <>{children}</>;
}