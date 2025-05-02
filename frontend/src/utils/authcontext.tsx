"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";

interface User {
    email: string;
    role: string;
} // first declaration of type

interface AuthContextType {
    user: User | null;
    logout: () => void; 
    prefillEmail: string | null;
    setPrefillEmail: (email: string | null) => void;
} // second type declaration & netting the first in side
// the function inside is void

const AuthContext = createContext<AuthContextType>({
    user: null,
    logout: () => {},
    prefillEmail: null,
    setPrefillEmail: () => {},
}); // now we see the initiation of the second type

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [prefillEmail, setPrefillEmail] = useState<string | null>(null);
    // another "user" entity

    // useEffect() responds to render-triggers, 
    // and those renders are often triggered by user actions.
    // runs once on mount, to check if the token exist, [] is the dependency array

    // onClick pulls the trigger,
    // useState loads the bullet,
    // and useEffect watches the smoke.
    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) return;

        try {
            const decode: any = jwtDecode(token);
            // I don’t know (or care) what type decode is—trust me, I’ll handle it.
            setUser({ email: decode.sub, role: decode.role});
        } catch (err) {
            console.error("Invalid token");
            localStorage.removeItem("token");
        } // if error - remove that token
    }, []); 

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
    }; // in case logout is called, do this

    return (
        <AuthContext.Provider value={{ user, logout, prefillEmail, setPrefillEmail}}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext); 
// the AuthContext can either be of 1 or 2 value