"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { createNewSession } from "@/utils/api";
import '../globals.css';

export default function ChatEntryPage() {
  const router = useRouter();

  useEffect(() => {
    (async () => {
      const token = localStorage.getItem("token") || "";
      const { success, data } = await createNewSession(token);
      if (success) router.replace(`/chat/${data.session_id}`);
      else alert("Failed to start new session.");
    })();
  }, []);

  return <div className="p-8 text-gray-500">Loading...</div>;
}