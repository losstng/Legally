import React, { useRef } from "react";

const FileUploader = () => {
    const fileInputRef = useRef<HTMLInputElement>(null) ;

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        alert (`File selected: ${file.name}`);
    };

    return (
        <div className="my-2">
            <label className="block text-sm font-medium mb-1">Attach a file (optional):</label>
            <input 
                type="file"
                ref={fileInputRef}
                className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
                onChange={handleFileChange} />
        </div>
    );
};

export default FileUploader;