import { useState } from "react";
import { fetchHistory } from '../../utils/api';

export default function HistoryList() {
  const [history, setHistory] = useState([]);

  const loadHistory = async () => {
    const data = await fetchHistory();
    setHistory(data.data || []);
  };

  return (
    <div className="mb-4">
      <button onClick={loadHistory} className="mb-2 p-2 bg-gray-200 rounded">Load History</button>
      <ul>
        {history.map((h: any) => (
          <li key={h.id}>
            Q: {h.question} <br />
            A: {h.answer} <br />
            <span className="text-xs text-gray-500">{h.timestamp}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}