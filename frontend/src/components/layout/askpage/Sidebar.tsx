"use client";
import { useEffect, useState } from "react";
import SidebarList from "./SidebarList";
import FileList from "@/components/chat/files/FileList";
import SidebarTabs from "./SidebarTabs";
import { fetchSessions } from "@/utils/api";

interface SidebarProps {
  onSelectSession: (id: number) => void;
}

export default function Sidebar({ onSelectSession }: SidebarProps) {
  const [activeTab, setActiveTab] = useState<"History" | "Files">("History");
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    if (activeTab === "History") {
      const loadSessions = async () => {
        const res = await fetchSessions();
        setSessions((res.data || []).map((s: any) => ({
          id: s.id,
          label: s.title,
        })));
      };
      loadSessions();
    }
  }, [activeTab]);

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      <SidebarTabs activeTab={activeTab} onTabChange={setActiveTab} />
      <div className="flex-1 overflow-y-auto p-2">
        {activeTab === "History" ? (
          <SidebarList items={sessions} onSelect={onSelectSession} />
        ) : (
          <FileList />
        )}
      </div>
    </div>
  );
}