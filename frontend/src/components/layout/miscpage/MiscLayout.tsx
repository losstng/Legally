"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import SidebarNavigation from "@/components/settings/Sidebar/SidebarNavigation";

export default function MiscLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  // Determine current active tab based on route path
  const activeTab: "Profile" | "Others" = pathname.includes("/profile") ? "Profile" : "Others";

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <SidebarNavigation
        activeTab={activeTab}
        onTabChange={(tab) => {
          window.location.href = tab === "Profile" ? "/settings/profile" : "/settings/legal";
        }}
      />

      {/* Main Content */}
      <main className="flex-1 p-8">
        {children}
      </main>
    </div>
  );
}