import { useState} from "react";
import { fetchFiles } from "@/utils/api";
import { deleteFile } from "@/utils/api";

export default function FileList() {
    const [files, setFiles] = useState([]);

    const loadFiles = async () => {
        const data = await fetchFiles();
        setFiles(data.data || []);
    };

    return (
        <div className="mb-4">
            <button onClick={loadFiles} className="mb-2 p-2 bg-gray-200 rounded"> Load Files</button>
            <ul>
                {files.map((f: any) => (
                    <li key={f.file_key}>
                        {f.filename} (uploaded: {f.uploaded})
                        <button
                        onClick={async () => {
                            await deleteFile(f.file_key);
                            setFiles(files => files.filter(file => file.file_key !== f.file_key));
                        }}
                        className="ml-2 text-red-600"
                        >Delete</button>  
                    </li>
                ))}
            </ul>
        </div>
    );
}