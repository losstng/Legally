"use client";
import React, { useState } from "react";

export default function ContactForm() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/misc/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();
      if (res.ok && data.success) {
        setSuccess("Your message has been sent.");
        setForm({ name: "", email: "", subject: "", message: "" });
      } else {
        setError(data.detail || "Failed to send message.");
      }
    } catch {
      setError("Network error.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white shadow-md rounded p-6 space-y-4">
      <h2 className="text-lg font-bold">Contact Us</h2>
      <input
        name="name"
        type="text"
        value={form.name}
        onChange={handleChange}
        placeholder="Your name"
        className="w-full p-2 border rounded"
        required
      />
      <input
        name="email"
        type="email"
        value={form.email}
        onChange={handleChange}
        placeholder="Your email"
        className="w-full p-2 border rounded"
        required
      />
      <input
        name="subject"
        type="text"
        value={form.subject}
        onChange={handleChange}
        placeholder="Subject"
        className="w-full p-2 border rounded"
        required
      />
      <textarea
        name="message"
        value={form.message}
        onChange={handleChange}
        placeholder="Your message"
        className="w-full p-2 border rounded h-32"
        required
      />
      {error && <p className="text-red-600 text-sm">{error}</p>}
      {success && <p className="text-green-600 text-sm">{success}</p>}
      <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">
        Send Message
      </button>
    </form>
  );
}