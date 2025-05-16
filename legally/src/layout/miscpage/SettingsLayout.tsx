"use client";
import React from "react";
import { usePathname, useRouter } from "next/navigation";
import SidebarNavigation from "@/components/settings/sidebar/SidebarNavigation";

export default function SettingsLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();

  const isOthers = pathname.includes("misc");
  const activeOthersTab = pathname.includes("privacy")
    ? "Privacy"
    : pathname.includes("terms")
    ? "Terms"
    : undefined;

  return (
  <div className="flex min-h-screen bg-gray-50">
    {/* Sidebar */}
    <SidebarNavigation
      activeTab={isOthers ? "Others" : "Profile"}
      onTabChange={(tab) => {
        const dest = tab === "Profile" ? "/settings/profile" : "/settings/misc/privacy";
        router.push(dest);
      }}
      activeOthersTab={activeOthersTab}
      onSelectOthersTab={(subtab) => {
        const dest = `/settings/misc/${subtab.toLowerCase()}`;
        router.push(dest);
      }}
    />

    {/* Main Content */}
    <main className="flex-1 px-8 py-10 overflow-y-auto">
      <div className="max-w-4xl mx-auto">{children}</div>
    </main>
  </div>
);
}