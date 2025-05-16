"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";

interface User {
  email: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  logout: () => void;
  prefillEmail: string | null;
  setPrefillEmail: (email: string | null) => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  logout: () => {},
  prefillEmail: null,
  setPrefillEmail: () => {},
  loading: true,
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [prefillEmail, setPrefillEmail] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      console.log("No token found");
      setLoading(false);
      return;
    }

    try {
      const decoded: any = jwtDecode(token);
      console.log("Decoded token:", decoded); // DEBUG

      if (decoded?.sub && decoded?.role) {
        setUser({ email: decoded.sub, role: decoded.role });
      } else {
        throw new Error("Token missing sub or role");
      }
    } catch (err) {
      console.error("Token error:", err);
      localStorage.removeItem("token");
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, logout, prefillEmail, setPrefillEmail, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);