import { useEffect, useState } from "react";
import { fetchSessionConversations } from '../../../utils/api';

export default function ChatSessionHistory({ sessionId }: { sessionId: number }) {
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    const loadEntries = async () => {
      const res = await fetchSessionConversations(sessionId);
      setEntries(res.data || []);
    };
    if (sessionId) loadEntries();
  }, [sessionId]);

  if (!entries.length) {
    return <p className="text-gray-500">No Q&A in this session yet though.</p>;
  }

  return (
    <ul className="space-y-4">
      {entries.map((entry) => (
        <li key={entry.id} className="p-4 border rounded">
          <p className="font-semibold"> Q: {entry.question}</p>
          <p className="mt-1 text-gray-700">A: {entry.answer}</p>
          <p className="text-xs text-gray-500 mt-2">{entry.timestamp}</p>
        </li>
      ))}
    </ul>
  );
}