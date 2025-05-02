import { useAuth } from "@/utils/authcontext"; // hypothetically
import Link from "next/link";

export default function SidebarFooter() {
  const { user, logout } = useAuth();

  return (
    <div className="px-4 py-4 border-t border-gray-800">
      {user ? (
        <>
          <button onClick={logout} className="w-full bg-red-600 hover:bg-red-700 py-2 rounded text-white font-semibold mb-3">
            Logout
          </button>
          <div className="text-sm text-gray-400 text-center space-x-2">
            <Link href="/settings/profile"><span className="hover:text-gray-200 cursor-pointer">Profile</span></Link>
            <span>&bull;</span>
            <Link href="/settings/security"><span className="hover:text-gray-200 cursor-pointer">Security</span></Link>
          </div>
        </>
      ) : (
        <Link href="/auth/login">
          <button className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded text-white font-semibold">
            Login
          </button>
        </Link>
      )}
    </div>
  );
}