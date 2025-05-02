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
    <div className="flex flex-col space-y-4 p-4 border-r border-gray-200 h-full bg-white min-w-[200px]">
      {/* Main Tabs */}
      <button
        onClick={() => onTabChange("Profile")}
        className={`w-full text-left px-4 py-2 rounded ${
          activeTab === "Profile"
            ? "bg-blue-600 text-white font-semibold"
            : "hover:bg-gray-100"
        }`}
      >
        Profile
      </button>
      <button
        onClick={() => onTabChange("Others")}
        className={`w-full text-left px-4 py-2 rounded ${
          activeTab === "Others"
            ? "bg-blue-600 text-white font-semibold"
            : "hover:bg-gray-100"
        }`}
      >
        Others
      </button>

      {/* Conditional Subtabs for Others */}
      {activeTab === "Others" && (
        <div className="ml-2 flex flex-col space-y-2 text-sm">
          <button
            onClick={() => onSelectOthersTab?.("Contact")}
            className={`text-left px-3 py-1 rounded ${
              activeOthersTab === "Contact"
                ? "bg-blue-100 text-blue-700 font-medium"
                : "hover:bg-gray-100"
            }`}
          >
            Contact
          </button>
          <button
            onClick={() => onSelectOthersTab?.("Privacy")}
            className={`text-left px-3 py-1 rounded ${
              activeOthersTab === "Privacy"
                ? "bg-blue-100 text-blue-700 font-medium"
                : "hover:bg-gray-100"
            }`}
          >
            Privacy Policy
          </button>
          <button
            onClick={() => onSelectOthersTab?.("Terms")}
            className={`text-left px-3 py-1 rounded ${
              activeOthersTab === "Terms"
                ? "bg-blue-100 text-blue-700 font-medium"
                : "hover:bg-gray-100"
            }`}
          >
            Terms of Use
          </button>
        </div>
      )}

      {/* Back to Chat */}
      <button
        onClick={() => (window.location.href = "/")}
        className="w-full text-left px-4 py-2 rounded text-sm text-gray-600 hover:text-black hover:bg-gray-100 mt-auto"
      >
        Back to Chat
      </button>
    </div>
  );
}