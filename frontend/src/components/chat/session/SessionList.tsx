"use client";
import { useEffect, useState } from "react";
import { fetchSessions } from "@/utils/api";

interface SessionListProps {
  onSelect: (id: number) => void;
}

export default function SessionList({ onSelect }: SessionListProps) {
  const [sessions, setSessions] = useState<
    { id: number; title: string; created_at: string }[]
  >([]);

  useEffect(() => {
    const loadSessions = async () => {
      const res = await fetchSessions();
      setSessions(res.data || []);
    };
    loadSessions();
  }, []);

  if (!sessions.length) {
    return <div className="text-gray-500 text-center mt-4">No sessions yet.</div>;
  }

  return (
    <ul className="space-y-2">
      {sessions.map((session) => (
        <li
          key={session.id}
          className="flex justify-between items-center px-3 py-2 rounded hover:bg-gray-200 cursor-pointer"
          onClick={() => onSelect(session.id)}
        >
          <span className="truncate">{session.title}</span>
        </li>
      ))}
    </ul>
  );
}