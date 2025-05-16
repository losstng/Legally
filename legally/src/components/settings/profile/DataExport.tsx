"use client";
import React from "react";
import { handleExport } from "@/utils/api";

export default function DataExport() {
  return (
    <button
      onClick={handleExport}
      className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
    >
      Export My Data
    </button>
  );
}