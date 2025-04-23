"use client";
import ChatBox from '../components/ChatBox';
import FileUploader from '../components/FileUploader';
import MessageBubble from '../components/MessageBubble';
import { useState } from 'react';

export default function Home() {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [file, setFile] = useState<File | null>(null);

  const handleSend = async (text: string) => {
    setMessages(prev => [...prev, { sender: "user", text }]);
    // TODO: Add API call here later to send message + file
  };

  const handleFileUpload = (selectedFile: File) => {
    setFile(selectedFile);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="flex-1 overflow-auto p-4">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} sender={msg.sender} text={msg.text} />
        ))}
      </div>
      <div className="p-2 flex items-center gap-2 border-t">
        <FileUploader onFileUpload={handleFileUpload} />
        <ChatBox onSend={handleSend} file={file} />
      </div>
    </div>
  );
}