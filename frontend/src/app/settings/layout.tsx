// app/settings/layout.tsx
import "@/styles/globals.css"; // if needed
import SidebarNavigation from "@/components/settings/Sidebar/SidebarNavigation";
import React from "react";

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Persistent Sidebar */}
      <SidebarNavigation
        activeTab={
          typeof window !== "undefined" && window.location.pathname.includes("legal")
            ? "Others"
            : "Profile"
        }
        onTabChange={(tab) => {
          if (typeof window !== "undefined") {
            window.location.href = tab === "Profile" ? "/settings/profile" : "/settings/legal";
          }
        }}
      />

      {/* Main content from /settings/profile or /settings/legal */}
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}