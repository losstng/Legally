import { useState } from "react";

export default function Sidebar() {
    const [tab, setTab] = useState<"history" | "files">("history");

    const historyList = [
        { id: 1, label: "gay"},
        { id: 2, label: "gay"},
    ];
    const fileList = [
        { id: "a", label: "gay.pdf"},
        { id: "b", label: "gay.pdf"},
    ];
    
}