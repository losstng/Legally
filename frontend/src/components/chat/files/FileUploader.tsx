import React, { useRef } from "react";

const FileUploader = ({ onFileUpload, file }) => { // props 1 callback and 1 object
    const fileInputRef = useRef<HTMLInputElement>(null); // useRef hold reference a DOM element or a mutable value between render, holding it as so
    // the initial value here is null
    // within <> is what type of object will the useRef refer to

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        // : here is TS type annotation - e has type
        // Change event - event fired when input changes
        // the event come from an HTML Input Element
        const selectedFile = e.target.files?.[0];
        // e.target - the DOM element defined above
        // the files or file to select the first one
        // ? is the optional chaining operator, asking if files exist or not to continue
        // [o] refer to the first item
        if (!selectedFile) return;
        
        if (!selectedFile.type.startsWith("application/")) {
            alert("Only document files are allowed (PDF, DOC, TXT).");
            return;
        }
        
        if (selectedFile.size > 5 * 1024 + 1024) {
            alert("File Must be smaller than 5MB.");
            return;
        }

        onFileUpload(selectedFile);

        fileInputRef.current!.value = "";
    };

    // we have a label above in attach file:
    // the input being an input element of HTML that varies based on OS and browser in ref
    // initially it is empty
    // then handle file change do the upload and selecting to show on UI
    // so after uploaded showcase the file defined in the class name above, and the file name under the span text
    return (
        <div className="my-2 flex items-center gap-2">
            <label className="block text-sm font-medium mb-1">Attach file:</label>
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                />
                {file && <span className="text-xs text-green-700">{file.name}</span>}
        </div>
    );
};

export default FileUploader;