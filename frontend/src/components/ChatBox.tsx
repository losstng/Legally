import { useState } from "react"; // function, named import
import MessageBubble from "./MessageBubble"; // so we are importing the objects or components defined before, default import
import FileUploader from "./FileUploader"; // components, default import
import { stringify } from "querystring"; // function, named import



const ChatBox = () => { //start of the code block
    const [messages, setMessages] = useState<{ role: string; text: string }[]> // so it ends here and [] is to declear that the object within {} is an []
    ([]); // declearing that the initial value is an empty array
    // The type in {} is a TypeScript annotation (for safety/checking).
    // [messages, setMessages] is array destructuring, unpacking what useState returns (like Python’s tuple unpacking).
    // declaring a destrucutring of what is in that array
    const [input, setInput] = useState(""); // state emptyness initally 

    const handleSend = () => { // the syntaxes are a bit verbose, so an arrow function assigned to a constant, with expected variables in ()
        if (!input.trim()) 
            return; // if result is empty, then !input is true, then we return early -> skipping everything, the return at a relatively coarse palce
        setMessages([...messages, {role: "user", text: input}]); //spread the current messages, and add the role and text equal the input defined before to append onto the message
        // add along the message the role and the input at the end apparently
        setInput("");

        // TODO: Call backend here and get response
        setTimeout(()=> { // ahh here is another code block
            setMessages(prev => [...prev, { role: "assisstant", text: "Fake reply from Legally." 
                // so here we are taking the prev out add the object with 2 stuff there at the end
            }]);
        }, 500); // then the expiry duration
        // setTimeout is used here to simulate backend latency; after 500ms, it adds a fake assistant message.
    };    
    
    return (
        <div className="flex flex-col h-full max-w-2xl mx-auto p-4"> {/* so this is how we comment, so the class name is usually written through the orders of stuffs */}
            <div className="flex-1 overflow-y-auto mb-4"> {/* so this class is then wrapped inside the above */}
                {messages.map((msg, i) =>( //map => the arry method for iteration, also the object iterations happen
                    <MessageBubble key={i} role={msg.role} text={msg.text} /> 
                ))}
                {/* essentially show the messages through iteration, and it is defined to shwo throught message bubble*/}
            </div>
            <FileUploader /> {/* when we have /> right at the end, it means nothing is wrapped inside it*/}
            <div className="flex-1 p-2 mt-2">
                <input
                    className="flex-1 p-2 border rounded"
                    type="text" 
                    value={input} 
                    onChange={e => setInput(e.target.value)}
                    placeholder="Ask Legally..."
                /> {/* input to be entered, essentially typable, and the type of it is text or string, whatver, also alwys in sync with React state*/}
                {/* also it seems as though, setInput is specifically to showcase input*/}
                {/* e is given as the event object by react*/}
                {/* e.target refers to the DOM element that triggered the event */}
                {/* e.target.value refers to the value of the DOM element that triggered the event */}
                <button onClick={handleSend} className="bg-blue-500 text-white px-4 py-2 rounded"> {/* ahhh the syntaxes here and above are different */}
                    Send {/* that's why we have handlSend within {}, it is the syntaxes are again fucking DIFFERENT WTF?*/}
                </button>
            </div>
        </div>
    );
};

export default ChatBox; // You can export one thing as the “default” from a module/file.

// You can export many things from one module/file by name.