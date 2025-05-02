"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/utils/authcontext";

export default function TopBar() {
  const router = useRouter();
  const { user } = useAuth();

  return (
    <header className="flex items-center justify-between h-16 px-6 border-b border-gray-200 bg-white shadow-sm">
      {/* New Chat button */}
      <button
        className="text-blue-600 font-bold hover:underline"
        onClick={() => router.push("/new-chat")}
      >
        + New Chat
      </button>

      {/* App Name */}
      <div className="text-2xl font-extrabold tracking-wider text-gray-800 select-none">
        Legally
      </div>

      {/* Theme Toggle (to be wired to context or state) */}
      <button
        className="rounded-full p-2 bg-gray-200 hover:bg-gray-300 transition"
        onClick={() => {
          // Integrate with theme toggle state/context
          alert("Theme toggle clicked!");
        }}
      >
        Theme
      </button>
    </header>
  );
}