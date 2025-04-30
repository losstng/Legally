import { useState } from "react";

const ChatBox = ({ onSend, file }) => { // props to be used later
    const [input, setInput] = useState(""); // first it is empty, no specific which format it should be

    const handleSend = () => {
        if (!input.trim() && !file) return;
        // so trim removes all white space leading to null
        // && is and in JS making conditions
        onSend(input); // onsend here is to be received, as it is prop
        setInput(""); // make input empty again
    };

    return (
        <div className="flex-1 p-2 mt-2 flex gap-2"> 
            <input 
            className="flex-1 p-2 border rounded"
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)} 
            placeholder="Ask Legally..." />
            {/* e is always the event object in react */}
            {/* target here input being typed */}
            {/* change to the value of the target */}
            <button onClick={handleSend} className="bg-blue-500 text-white px-4 py-2 rounded">
                {/* the onclick here is a  property of the button */}
                Send
            </button>
        </div>
    )
};

export default ChatBox;