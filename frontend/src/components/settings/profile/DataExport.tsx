"use client";
import React from "react";

export default function DataExport() {
  const handleExport = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/export`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) {
        throw new Error("Failed to export data");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "legally_export.csv";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Export failed:", err);
      alert("Could not export your data.");
    }
  };

  return (
    <button
      onClick={handleExport}
      className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
    >
      Export My Data
    </button>
  );
}