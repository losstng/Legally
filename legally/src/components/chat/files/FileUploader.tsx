import React, { useRef } from "react";

const FileUploader = ({ onFileUpload, file }) => { 
    const fileInputRef = useRef<HTMLInputElement>(null); 

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;
        
        const fileExt = selectedFile.name.split(".").pop()?.toLowerCase();
        if (!["pdf", "doc", "docx", "txt"].includes(fileExt)) {
            alert("Unsupported file format.");
            return;
        }
        
        if (selectedFile.size > 5 * 1024 * 1024) {
            alert("File Must be smaller than 5MB.");
            return;
        }

        onFileUpload(selectedFile);

        fileInputRef.current!.value = "";
    };

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