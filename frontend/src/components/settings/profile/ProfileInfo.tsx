"use client";
import { useEffect, useState } from "react";

export default function ProfileInfo() {
  const [profile, setProfile] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        const data = await res.json();
        if (res.ok && data.success) {
          setProfile(data.data);
        } else {
          setError(data.detail || data.error || "Failed to fetch profile.");
        }
      } catch {
        setError("Network error.");
      }
    };
    loadProfile();
  }, []);

  if (error) return <p className="text-red-600">{error}</p>;
  if (!profile) return <p className="text-gray-500">Loading profile...</p>;

  return (
    <div className="bg-white shadow rounded p-6">
      <h2 className="text-lg font-bold mb-4">Your Profile</h2>
      <ul className="space-y-2">
        <li><strong>Name:</strong> {profile.name}</li>
        <li><strong>Email:</strong> {profile.email}</li>
        <li><strong>Age:</strong> {profile.age}</li>
        <li><strong>Role:</strong> {profile.role}</li>
      </ul>
    </div>
  );
}