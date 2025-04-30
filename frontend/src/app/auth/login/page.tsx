import LoginForm from "@/components/auth/LoginForm";
import AuthLayout from "@/components/layout/authpage/AuthLayout";

export default function LoginPage() {
    return(
        <AuthLayout>
            <LoginForm/>
        </AuthLayout>
    );
}