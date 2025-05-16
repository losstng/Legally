"use client";
import { useEffect, useState } from "react";
import { fetchFiles, deleteFile } from "@/utils/api";
import SidebarList from "../../../layout/askpage/SidebarList";

export default function FileList() {
  const [files, setFiles] = useState<{ id: string; label: string }[]>([]);

  useEffect(() => {
    const loadFiles = async () => {
      const data = await fetchFiles();
      const transformed = (data.data || []).map((file: any) => ({
        id: file.file_key,
        label: `${file.filename} (uploaded: ${new Date(file.uploaded).toLocaleString()})`,
      }));
      setFiles(transformed);
    };

    loadFiles();
  }, []);

  const handleDelete = async (fileKey: string) => {
    await deleteFile(fileKey);
    setFiles((prev) => prev.filter((file) => file.id !== fileKey));
  };

  return <SidebarList items={files} onDelete={handleDelete} />;
}