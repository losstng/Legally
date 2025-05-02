interface SidebarTabsProps {
    activeTab: "History" | "Files";
    onTabChange: (tab: "History" | "Files") => void;
  }
  
  export default function SidebarTabs({ activeTab, onTabChange }: SidebarTabsProps) {
    return (
      <div className="flex justify-between p-4 border-b border-gray-800">
        <button
          className={`flex-1 px-4 py-2 rounded-l ${
            activeTab === "History" ? "bg-gray-800 font-semibold" : "bg-gray-900 hover:bg-gray-800"
          }`}
          onClick={() => onTabChange("History")}
        >
          History
        </button>
        <button
          className={`flex-1 px-4 py-2 rounded-r ${
            activeTab === "Files" ? "bg-gray-800 font-semibold" : "bg-gray-900 hover:bg-gray-800"
          }`}
          onClick={() => onTabChange("Files")}
        >
          Files
        </button>
      </div>
    );
  }