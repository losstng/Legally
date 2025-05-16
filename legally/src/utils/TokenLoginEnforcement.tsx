"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function TokenLoginEnforcement({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      router.replace("/"); // Already logged in? Skip login.
    } else {
      setChecking(false); // Not logged in? Let them through.
    }
  }, []);

  if (checking) return null; // Wait until we know what's up.
  return <>{children}</>;
}