import React from "react";
import { AuthProvider } from "@/utils/authcontext";

// layout.tsx
export const metadata = {
  title: "Legally",
  description: "Your Legal assistantn",
};
export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body className= "bg-gray-100 text-gray- 900">
        <AuthProvider>  
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}