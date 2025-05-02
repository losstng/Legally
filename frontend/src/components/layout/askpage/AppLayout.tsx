"use client";
import { useState } from "react";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";
import MainChat from "./MainChat";
import Brandfooter from "./BrandFooter";

export default function AppLayout() {
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);

  return (
    <div className="flex h-screen w-screen bg-gradient-to-tr from-gray-50 to-blue-100">
      {/* Sidebar */}
      <aside className="w-72 bg-gray-900 text-white flex flex-col justify-between">
        <Sidebar onSelectSession={setActiveSessionId} />
        <Brandfooter />
      </aside>

      {/* Main */}
      <main className="flex-1 flex flex-col relative bg-white rounded-l-3xl shadow-lg overflow-hidden">
        <TopBar />
        <div className="flex-1 overflow-y-auto p-4">
          {activeSessionId ? (
            <MainChat sessionId={activeSessionId} />
          ) : (
            <div className="text-center text-gray-400 mt-20">Select a session to begin</div>
          )}
        </div>
      </main>
    </div>
  );
}