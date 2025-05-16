"use client";
import { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import MainChat from "./MainChat";

export default function AppLayout({ sessionId }: { sessionId: number | null }) {
  const [activeSessionId, setActiveSessionId] = useState<number | null>(sessionId);

  // Handle session selection from Sidebar
  const handleSessionSelect = (id: number) => {
    setActiveSessionId(id);
  };

  return (
    <div className="flex h-screen w-screen bg-gradient-to-tr from-gray-50 to-blue-100">
      {/* Sidebar */}
      <aside className="w-72 bg-gray-900 text-white flex flex-col justify-between">
        <Sidebar onSelectSession={handleSessionSelect} />
      </aside>

      {/* MainChat renders with active session */}
      <main className="flex-1 flex flex-col relative bg-white rounded-l-3xl shadow-lg overflow-hidden">
        <MainChat sessionId={activeSessionId} />
      </main>
    </div>
  );
}