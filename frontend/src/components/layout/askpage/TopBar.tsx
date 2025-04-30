import Link from "next/link";

export default function TopBar() {
    return (
        <header className="flex items-center justify-between h-16 px-8 border-b border-gray-200 bg-white shadow-sm">
            {/* New chat button on the left */}
            <Link href="/new-chat">
                <button className="text-blue-600 font-bold hover:underline">
                    + New Chat
                </button>
            </Link>

            {/* App Name in the center */}
            <div className="text-2xl font-extrabold tracking-wider text-gray-800 select-none">
                Legally
            </div>

            {/* Theme toggle on the Right*/}
            <button 
                className="rounded-full p-2 bg-gray-200 hover:bg-gray-300 transition"
                onClick={() => {
                    // TODO: integrate with real theme toggle logic alert("theme toggle clicked!");
                }}>
                    Theme
                </button>
        </header>
    );
}