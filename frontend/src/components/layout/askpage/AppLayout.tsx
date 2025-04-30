import React from "react";

export default function AppLayout({ children }: { children?: React.ReactNode}) {
                    //the function receives an object that may (?) have a property children, whose type is React.ReactNode.
                    // Node is the broadest type for anything you can render in React
                    // this compnent accepts a prop named children (optiona), and if present, it should be something React can render
    return (
        <div className="flex h-screen w-screen bg-gradient-to-tr from-gray-50 to-blue-100">
            {/*SideBar here*/}
            <aside className="w-72 bg-gray-900 text-white flex flex-col justify-between">
                {/* Top: Selector & List*/}
                <div>
                    <div className="flex justify-between px-4 py-6 border-b border-gray-800">
                        {/* Sidebar Tabs (History/Files) */}
                        <button className="px-4 py-2 rounded bg-gray-800 hover:bg-gray-700">History</button>
                        <button className="px-4 py-2 rounded bg-gray-800 hover:bg-gray-700">Files</button>
                    </div>
                    {/* List */}
                    <div className="flex-1 overflow-y-auto px-4 py-2">
                        {/* Place Holder for list items */}
                        <div className="text-gray-400 text-center mt-8">No items yet</div>
                    </div>
                </div>
                {/* Bottom: Login & Misc */}
                <div className="px-4 py-4 border-t border-gray-800">
                    <button className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded text-white font-semibold">
                        Login
                    </button>
                    {/* Misc links go here*/}
                </div>
            </aside>

            {/* Main Content */}
            <main className=" flex-1 flex flex-col relative bg-white rounded-l-3xl shadow-lg overflow-hidden">
                {/* Top Bar */}
                <div className="flex items-center justify-betweem h-16 px-8 border-b border-gray-200 bg-white shadow-sm">
                    <button className="text-blue-600 font-bold">+ New Chat</button>
                    <div className="text-2xl font-extrabold tracking-wider text-gray-800">Legally</div>
                    <button className="rounded-full p-2 bg-gray-200 hover: bg-gray-300 transition">Theme</button>
                </div>
                
                {/* Chat/Main Area */}
                <div className="flex-1 px-8 py-6 overflow-y-auto">
                    {/* This is where the chat or children will go */}
                    <div className="text-gray-400 text-center mt-12">Your chat goes here</div>
                    {children}
                </div>

                {/* Chatbox */}
                <div className="flex items-center p-4 border-t border-gray-200 bg-gray-50">
                    <button className="mr-3 text-xl px-2 py-1 rounded hover:bg-gray-200 transition">Files</button>
                    <input
                        className="flex-1 p-2 rounded border mx-2 focus:outline-none focus:ring-2 focus:ring-blue-200"
                        placeholder="What problem(s) do you have?"
                        disabled 
                    />
                    <button className="ml-3 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition font-semibold">
                        Send
                    </button>
                </div>
            </main>
        </div>
    );
}