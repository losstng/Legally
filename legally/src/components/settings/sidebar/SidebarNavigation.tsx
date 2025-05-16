"use client";
import React from "react";

interface SidebarNavigationProps {
  activeTab: "Profile" | "Others";
  onTabChange: (tab: "Profile" | "Others") => void;
  onSelectOthersTab?: (subtab: "Contact" | "Privacy" | "Terms") => void;
  activeOthersTab?: "Contact" | "Privacy" | "Terms";
}

export default function SidebarNavigation({
  activeTab,
  onTabChange,
  onSelectOthersTab,
  activeOthersTab,
}: SidebarNavigationProps) {
  return (
  <div className="flex flex-col p-4 space-y-3 bg-white border-r border-gray-200 h-full min-w-[220px]">
    {/* Main Tabs */}
    <div className="space-y-2">
      <button
        onClick={() => onTabChange("Profile")}
        className={`w-full text-left px-4 py-2 rounded-md transition ${
          activeTab === "Profile"
            ? "bg-blue-600 text-white font-semibold shadow-sm"
            : "text-gray-700 hover:bg-gray-100"
        }`}
      >
        Profile
      </button>
      <button
        onClick={() => onTabChange("Others")}
        className={`w-full text-left px-4 py-2 rounded-md transition ${
          activeTab === "Others"
            ? "bg-blue-600 text-white font-semibold shadow-sm"
            : "text-gray-700 hover:bg-gray-100"
        }`}
      >
        Others
      </button>
    </div>

    {/* Conditional Subtabs for 'Others' */}
    {activeTab === "Others" && (
      <div className="mt-1 ml-3 pl-1 border-l border-gray-100 space-y-1">
        <button
          onClick={() => onSelectOthersTab?.("Privacy")}
          className={`w-full text-left px-3 py-1 rounded-md text-sm transition ${
            activeOthersTab === "Privacy"
              ? "bg-blue-100 text-blue-700 font-medium"
              : "text-gray-700 hover:bg-gray-100"
          }`}
        >
          Privacy Policy
        </button>
        <button
          onClick={() => onSelectOthersTab?.("Terms")}
          className={`w-full text-left px-3 py-1 rounded-md text-sm transition ${
            activeOthersTab === "Terms"
              ? "bg-blue-100 text-blue-700 font-medium"
              : "text-gray-700 hover:bg-gray-100"
          }`}
        >
          Terms of Use
        </button>
      </div>
    )}

    {/* Spacer */}
    <div className="flex-grow" />

    {/* Back to Chat */}
    <button
      onClick={() => (window.location.href = "/")}
      className="w-full text-left px-4 py-2 rounded-md text-sm text-gray-500 hover:text-black hover:bg-gray-100 transition"
    >
      ← Back to Chat
    </button>
  </div>
);
}