"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import {
  fetchFiles,
  fetchSessions,
  deleteFile,
  deleteSession,
  renameFile,
  renameSession,
} from "@/utils/api";
import { useRouter } from "next/navigation";

interface SidebarProps {
  onSelectSession: (id: number) => void;
}

export default function Sidebar({ onSelectSession }: SidebarProps) {
  const [activeTab, setActiveTab] = useState<"History" | "Files">("History");
  const [sessions, setSessions] = useState([]);
  const [files, setFiles] = useState([]);
  const [editingSessionId, setEditingSessionId] = useState<number | null>(null);
  const [editingFileKey, setEditingFileKey] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    if (activeTab === "History") {
      const loadSessions = async () => {
        const res = await fetchSessions();
        setSessions(
          (res.data || []).map((s: any) => ({
            id: s.id,
            label: s.title,
          }))
        );
      };
      loadSessions();
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === "Files") {
      const loadFiles = async () => {
        const res = await fetchFiles();
        setFiles(res.data || []);
      };
      loadFiles();
    }
  }, [activeTab]);

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      {/* Tabs */}
      <div className="flex justify-between p-4 border-b border-gray-800">
        <button
          className={`flex-1 px-4 py-2 rounded-l ${
            activeTab === "History"
              ? "bg-gray-800 font-semibold"
              : "bg-gray-900 hover:bg-gray-800"
          }`}
          onClick={() => setActiveTab("History")}
        >
          History
        </button>
        <button
          className={`flex-1 px-4 py-2 rounded-r ${
            activeTab === "Files"
              ? "bg-gray-800 font-semibold"
              : "bg-gray-900 hover:bg-gray-800"
          }`}
          onClick={() => setActiveTab("Files")}
        >
          Files
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-2">
        {activeTab === "History" ? (
          sessions.length > 0 ? (
            <ul className="space-y-2">
              {sessions.map((item: any) => (
                <li
  key={item.id}
  className="flex justify-between items-center px-3 py-2 rounded hover:bg-gray-800 transition group"
>
  {editingSessionId === item.id ? (
  <input
    className="bg-transparent text-white w-full truncate focus:outline-none border-b border-gray-600 focus:border-white"
    value={item.label}
    onChange={(e) => {
      const updated = [...sessions];
      updated.find((s) => s.id === item.id)!.label = e.target.value;
      setSessions(updated);
    }}
    onBlur={async (e) => {
      await renameSession(item.id, e.target.value);
      setEditingSessionId(null);
    }}
    autoFocus
  />
) : (
  <>
    <div className="flex-1 truncate">
      <span>{item.label}</span>
    </div>
    <button
      className="ml-2 text-xs text-blue-400 hover:text-blue-200"
      onClick={(e) => {
  e.stopPropagation();
  router.push(`/chat/${item.id}`);
}}
    >
      Select
    </button>
  </>
)}

  <button
    className="ml-2 text-xs text-gray-400 hover:text-white"
    onClick={(e) => {
      e.stopPropagation();
      setEditingSessionId(item.id);
    }}
  >
    Rename
  </button>

  <button
    onClick={async (e) => {
      e.stopPropagation();
      await deleteSession(item.id);
      setSessions((s) => s.filter((sess) => sess.id !== item.id));
    }}
    className="text-sm text-red-400 hover:text-red-200 ml-2"
  >
    Delete
  </button>
</li>
              ))}
            </ul>
          ) : (
            <div className="text-gray-500 text-center mt-6">No items, ... yet</div>
          )
        ) : files.length > 0 ? (
          <ul className="space-y-2">
            {files.map((file: any) => (
              <li
                key={file.file_key}
                className="flex justify-between items-center px-3 py-2 rounded hover:bg-gray-800 transition group cursor-default"
              >
                {editingFileKey === file.file_key ? (
                  <input
                    className="bg-transparent text-white w-full truncate focus:outline-none border-b border-gray-600 focus:border-white"
                    value={file.filename}
                    onChange={(e) => {
                      const updated = [...files];
                      updated.find((f) => f.file_key === file.file_key)!.filename =
                        e.target.value;
                      setFiles(updated);
                    }}
                    onBlur={async (e) => {
                      await renameFile(file.file_key, e.target.value);
                      setEditingFileKey(null);
                    }}
                    autoFocus
                  />
                ) : (
                  <div className="flex-1 truncate">
                    <span>{file.filename}</span>
                    <button
                      className="ml-2 text-xs text-gray-400 hover:text-white"
                      onClick={() => setEditingFileKey(file.file_key)}
                    >
                      Rename
                    </button>
                  </div>
                )}
                <button
                  onClick={async () => {
                    await deleteFile(file.file_key);
                    setFiles((f) => f.filter((x) => x.file_key !== file.file_key));
                  }}
                  className="text-sm text-red-400 hover:text-red-200"
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-gray-500 text-center mt-6">No uploaded files yet.</div>
        )}
      </div>

      {/* Footer */}
      <div className="px-4 py-4 border-t border-gray-800">
        <Link href="/settings/profile">
          <button className="w-full bg-gray-700 hover:bg-gray-600 py-2 rounded text-white font-semibold">
            Settings
          </button>
        </Link>
      </div>
    </div>
  );
}