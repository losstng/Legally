"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import { requestPasswordChange } from "@/utils/api";

export default function PasswordChange() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleRequestChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const { success, email, data } = await requestPasswordChange(currentPassword, newPassword);
  
      if (success && email) {
        router.push(`/auth/verify?email=${encodeURIComponent(email)}&action=change_password&new_password=${encodeURIComponent(newPassword)}`);
      } else {
        setError(data.detail || "Failed to initiate password change.");
      }
    } catch (err: any) {
      setError(err.message || "Network error.");
    }
  };

  return (
    <form onSubmit={handleRequestChange} className="max-w-md mx-auto mt-10 p-6 border rounded bg-white shadow">
      <h2 className="text-lg font-bold mb-4">Change Password</h2>
      <input
        type="password"
        placeholder="Current Password"
        className="w-full p-2 border rounded mb-4"
        value={currentPassword}
        onChange={(e) => setCurrentPassword(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="New Password"
        className="w-full p-2 border rounded mb-4"
        value={newPassword}
        onChange={(e) => setNewPassword(e.target.value)}
        required
      />
      {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
      <button type="submit" className="bg-blue-600 text-white py-2 px-4 rounded">
        Request Change
      </button>
    </form>
  );
}