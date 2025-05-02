"use client";
import { useEffect, useState } from "react";
import ChatBox from "@/components/chat/ChatBox";
import FileUploader from "@/components/chat/files/FileUploader";
import MessageBubble from "@/components/chat/MessageBubble";
import { fetchSessionConversations } from "@/utils/api";

export default function MainChat({ sessionId }: { sessionId: number }) {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [file, setFile] = useState<File | null>(null);

  useEffect(() => {
    const loadSessionMessages = async () => {
      const res = await fetchSessionConversations(sessionId);
      const entries = res.data || [];

      const formatted = entries.map((entry: any) => [
        { sender: "user", text: entry.question },
        { sender: "bot", text: entry.answer },
      ]).flat();

      setMessages(formatted);
    };

    if (sessionId) loadSessionMessages();
  }, [sessionId]);

  const handleSend = async (text: string) => {
    if (!text.trim() && !file) return;

    setMessages(prev => [...prev, { sender: "user", text }]);

    const formData = new FormData();
    formData.append("question", text);
    if (file) formData.append("file", file);
    formData.append("chat_session_id", String(sessionId));

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/ask/ask`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.success) {
        setMessages(prev => [...prev, { sender: "bot", text: data.data.answer }]);
      } else {
        setMessages(prev => [...prev, { sender: "bot", text: data.error || "Something went wrong." }]);
      }
    } catch {
      setMessages(prev => [...prev, { sender: "bot", text: "Network/server error." }]);
    }

    setFile(null);
  };

  const handleFileUpload = (selected: File) => setFile(selected);

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} role={msg.sender} text={msg.text} />
        ))}
      </div>
      <div className="p-4 border-t flex items-center gap-2">
        <FileUploader onFileUpload={handleFileUpload} file={file} />
        <ChatBox onSend={handleSend} file={file} />
      </div>
    </div>
  );
}