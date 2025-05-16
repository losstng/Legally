"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/utils/authcontext";
import ChatBox from "@/components/chat/ChatBox";
import FileUploader from "@/components/chat/files/FileUploader";
import MessageBubble from "@/components/chat/MessageBubble";
import { fetchSessionConversations, createNewSession, submitChatMessage } from "@/utils/api";

export default function MainPanel({ sessionId }: { sessionId?: number | null}) {
  const router = useRouter();
  const { user } = useAuth();
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [currentSessionId, setCurrentSessionId] = useState<number | null>(sessionId ?? null);

  useEffect(() => {
    if (!currentSessionId) return;
    const loadSessionMessages = async () => {
      const res = await fetchSessionConversations(currentSessionId);
      const entries = res.data || [];
      const formatted = entries.flatMap((entry: any) => [
        { sender: "user", text: entry.question },
        { sender: "bot", text: entry.answer },
      ]);
      setMessages(formatted);
    };
    loadSessionMessages();
    }, [currentSessionId]);

    const handleSend = async (text: string) => {
      if (!text.trim() && !file) return;
      setMessages(prev => [...prev, { sender: "user", text }]);
    
      let id = currentSessionId;
    
      if (!id) {
        const token = localStorage.getItem("token") || "";
        const { success, data } = await createNewSession(token);
        if (success) {
          id = data.session_id;
          setCurrentSessionId(id);
          router.push(`/chat/${data.session_id}`);
        } else {
          setMessages(prev => [...prev, { sender: "bot", text: "Failed to create new session." }]);
          return;
        }
      }
    
      const formData = new FormData();
      formData.append("question", text);
      if (file) formData.append("file", file);
      formData.append("chat_session_id", String(id));
    
      try {
        const { success, data } = await submitChatMessage(formData);
        setMessages(prev => [
  ...prev,
  { sender: "bot", text: success ? data.data.answer : (data.error || "Something went wrong.") }
])
      } catch {
        setMessages(prev => [...prev, { sender: "bot", text: "Network/server error." }]);
      }
    
      setFile(null);
    };
    

    const handleNewChat = async () => {
      const token = localStorage.getItem("token") || "";
      const { success, data } = await createNewSession(token);
      console.log("New session response:", data);
      if (success) router.push(`/chat/${data.session_id}`);
      else alert(data.detail || "Failed to create new session.");
    };

  return (
    <div className="flex flex-col h-full w-full relative bg-gray-50">
      {/* TopBar */}
      <header className="flex items-center justify-between h-16 px-6 border-b border-gray-200 bg-white shadow-sm">
        <button
          className="text-blue-600 font-bold hover:underline"
          onClick={handleNewChat}
        >
          + New Chat
        </button>
        <div className="text-2xl font-extrabold tracking-wider text-gray-800 select-none">
          Legally
        </div>
        <button
          className="rounded-full p-2 bg-gray-200 hover:bg-gray-300 transition"
          onClick={() => alert("Theme toggle clicked!")}
        >
          Theme
        </button>
      </header>

      {/* Chat Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} role={msg.sender} text={msg.text} />
        ))}
      </div>

      {/* Chat Input */}
      <div className="p-4 border-t flex items-center gap-2">
        <FileUploader onFileUpload={setFile} file={file} />
        <ChatBox onSend={handleSend} file={file} />
      </div>

      {/* Footer Branding */}
      <div className="absolute bottom-6 right-10 opacity-60 select-none pointer-events-none">
        <span className="text-2xl font-bold tracking-wide text-gray-400">Legally</span>
      </div>
    </div>
  );
}