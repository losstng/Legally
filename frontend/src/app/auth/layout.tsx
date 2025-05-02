// app/auth/layout.tsx
import AuthLayout from "@/components/layout/authpage/AuthLayout";

export default function AuthRouteLayout({ children }: { children: React.ReactNode }) {
  return <AuthLayout>{children}</AuthLayout>;
}