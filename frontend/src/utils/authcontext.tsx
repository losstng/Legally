"use client";
import { createContext, useContext, useEffect, useState } from "react";
import jwt_decode from "jwt-decode";

interface User {
    email: string;
    role: string;
}

interface AuthContextType {
    user: User | null;
    logout: () => void; 
}

const AuthContext = createContext<AuthContextType>({
    user: null,
    logout: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) return;

        try {
            const decode: any = jwt_decode(token);
            setUser({ email: decode.sub, role: decode.role});
        } catch (err) {
            console.error("Invalid token");
            localStorage.removeItem("token");
        }
    }, []);

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, logout}}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);