interface MessageBubbleProps { // typescript interface
    role: string;
    text: string;
} // declaring the shape - required fieds of the props this component will accept
// both role and text need to be strings

const MessageBubble = ({role, text }: MessageBubbleProps) => {
    // so the props in role and text are defined in the above
    // props are case and letter specific

    const isUser = role === "user"; // to be used later
    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-2`}>
             {/* flex - horizontal layout arrangement*/}
             {/* Here, ${isUser ? ...} dynamically chooses a class depending on the value of isUser. */}
             {/* damn so ` and $ then : is just dynamically allow the function to react*/}
             {/* so $ then ? then : are ternary operator unique to TS, especially in True or False */}
             {/* so the one after ? is always True, and after : is always False*/}
             {/* essentially an inline "if-else" */}
            <div 
                className={`px-4 py-2 rounded-lg max-w-[70%] ${
                    isUser
                        ? "bg-blue-500 text-white"
                        : "bg-gray-200 text-gray-800"
                }`}
            >
            {text}
            </div>    
        </div>
    );
};

export default MessageBuble;