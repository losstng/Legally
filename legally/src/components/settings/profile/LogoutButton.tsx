"use client";
import { useAuth } from "@/utils/authcontext";
import { useRouter } from "next/navigation";

export default function LogoutButton() {
    const { logout } = useAuth();
    const router = useRouter();

    const handleLogout = () => {
        logout();
        router.push("/auth/login");
    };

    return (
        <button
            onClick={handleLogout}
            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
            Logout        
        </button>
    );
}