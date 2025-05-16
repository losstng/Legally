"use client";
import { useParams } from "next/navigation";
import AppLayout from "@/layout/askpage/AppLayout";
import '../../globals.css';

export default function ChatSessionPage() {
  const { id } = useParams();
  const sessionId = id ? Number(id) : null;

  return <AppLayout sessionId={isNaN(sessionId!) ? null : sessionId} />;
}