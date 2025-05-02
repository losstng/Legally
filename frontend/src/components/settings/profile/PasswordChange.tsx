"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function PasswordChange() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleRequestChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const token = localStorage.getItem("token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/settings/request-password-change`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      const data = await res.json();
      if (res.ok && data.success) {
        const email = data.data.email;
        router.push(`/auth/verify?email=${encodeURIComponent(email)}&action=change_password&new_password=${encodeURIComponent(newPassword)}`);
      } else {
        setError(data.detail || "Failed to initiate password change.");
      }
    } catch {
      setError("Network error.");
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