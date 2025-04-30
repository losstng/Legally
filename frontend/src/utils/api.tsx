const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://glorious-carnival-694j5w4w7qv9hxq9q-8000.app.github.dev";

export async function fetchFiles() {
  const res = await fetch(`${API_URL.replace(/\/$/, "")}/ask/files`);
  return res.json();
}

export async function deleteFile(file_key: string) {
    const res = await fetch(
        `${API_URL.replace(/\/$/, "")}/ask/files/${file_key}`,
        { method: "DELETE" }
    );
    return res.json()
}

export async function fetchHistory() {
    const res = await fetch(`${API_URL.replace(/\/$/, "")}/ask/history`);
    return res.json();
}