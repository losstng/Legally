import { jwtDecode } from "jwt-decode";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://glorious-carnival-694j5w4w7qv9hxq9q-8000.app.github.dev";

// ----------------------------
// /ask Routes
// ----------------------------

export async function fetchFiles() {
  const token = localStorage.getItem("token") || "";
  const res = await fetch(`${API_URL.replace(/\/$/, "")}/ask/files`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}

export async function renameFile(file_key: string, newName: string) {
  const token = localStorage.getItem("token") || "";
  const formData = new FormData();
  formData.append("new_name", newName);

  const res = await fetch(`${API_URL}/ask/files/${file_key}/rename`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  return res.json();
}

export async function deleteFile(file_key: string) {
  const token = localStorage.getItem("token") || "";
  const res = await fetch(`${API_URL.replace(/\/$/, "")}/ask/files/${file_key}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}

export async function fetchSessionConversations(sessionId: number) {
  const token = localStorage.getItem("token") || "";
  const res = await fetch(`${API_URL}/ask/session/${sessionId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}


export async function fetchSessions() {
  const token = localStorage.getItem("token") || "";
  const res = await fetch(`${API_URL.replace(/\/$/, "")}/ask/sessions`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}

export async function createNewSession(token: string) {
  const res = await fetch(`${API_URL}/ask/new-session`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  return { success: res.ok && data.success, data: data.data };
}

export async function renameSession(sessionId: number, title: string) {
  const token = localStorage.getItem("token") || "";
  const formData = new FormData();
  formData.append("title", title);

  const res = await fetch(`${API_URL}/ask/session/${sessionId}/rename`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  return res.json();
}

export async function deleteSession(sessionId: number) { 
  const token = localStorage.getItem("token") || "";
  const res = await fetch(`${API_URL}/ask/session/${sessionId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

export async function submitChatMessage(formData: FormData) {
  const token = localStorage.getItem("token") || "";
  const res = await fetch(`${API_URL}/ask/ask`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: formData,
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

// ----------------------------
// /auth Routes
// ----------------------------

export async function loginUser(email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

export async function registerUser(payload: {
  name: string;
  age: number;
  email: string;
  password: string;
}) {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}


export async function verifyOTP(email: string, otp: string) {
  const res = await fetch(`${API_URL}/auth/verify-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp }),
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

export async function requestPasswordReset(email: string) {
  const res = await fetch(`${API_URL}/auth/forgot-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

export async function resetUserPassword(email: string, otp: string, newPassword: string) {
  const res = await fetch(`${API_URL}/auth/reset-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp, new_password: newPassword }),
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

export async function handleExport() {
  try {
    const token = localStorage.getItem("token") || "";
    const res = await fetch(`${API_URL}/auth/export`, {
      method: "GET",
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) throw new Error("Failed to export data");

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "legally_export.csv";
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  } catch (err) {
    console.error("Export failed:", err);
    alert("Could not export your data.");
  }
}

// ----------------------------
// /users Routes
// ----------------------------

export async function fetchUserProfile() {
  const token = localStorage.getItem("token");
  const res = await fetch(`${API_URL}/users/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

export async function requestPasswordChange(currentPassword: string, newPassword: string) {
  const token = localStorage.getItem("token");
  const res = await fetch(`${API_URL}/users/request-password-change`, {
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
  let email = null;

  if (res.ok && data.success) {
    try {
      const decoded: any = jwtDecode(token!);
      email = decoded?.sub || null;
    } catch {
      throw new Error("Failed to decode token.");
    }
  }

  return { success: res.ok && data.success, email, data };
}

export async function confirmPasswordChange(token: string, newPassword: string) {
  const res = await fetch(`${API_URL}/users/change-password`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ new_password: newPassword }),
  });
  return res.ok;
}

export async function deleteUser(token: string) {
  const res = await fetch(`${API_URL}/users/delete-user`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
  return res.ok;
}

export async function requestAccountDeletion(email: string) {
  const res = await fetch(`${API_URL}/users/request-delete`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  const data = await res.json();
  return { success: res.ok && data.success, data };
}

// ----------------------------
// /misc Routes
// ----------------------------

export async function submitContactForm(form: {
  name: string;
  email: string;
  subject: string;
  message: string;
}) {
  const res = await fetch(`${API_URL}/misc/contact`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(form),
  });

  const data = await res.json();
  return { success: res.ok && data.success, data };
}