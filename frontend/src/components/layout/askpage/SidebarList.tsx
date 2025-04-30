interface SidebarListProps {
    items: { id: string | number; label: string}[];
    onDelete?: (id: string | number) => void;
}

export default function SidebarList({ items, onDelete }: SidebarListProps) {
    if (!items.length) {
        return (
            <div className="text-gray-500 text-center mt-6">
                No items, ... yet
            </div>
        );
    }

    return(
        <ul className="space-y-2">
            {items.map((item) => (
                <li
                key={item.id}
                className="flex justify-between items-center px-3 py-2 rounded hover:bg-gray-800 transition group cursor-pointer"
                >
                    <span>{item.label}</span>
                    {onDelete && (
                        <button
                            onClick={() => onDelete(item.id)}
                            className="text-sm text-red-400 opacity-0 group-hover:opacity-100 transition"
                        >
                            Delete
                        </button>    
                    )}
                </li>
            ))}
        </ul>
    );
}