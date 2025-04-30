import ForgotPasswordForm from "@/components/auth/ForgotPasswordForm";
import AuthLayout from "@/components/layout/authpage/AuthLayout";

export default function ForgotPage() {
    return (
        <AuthLayout>
            <ForgotPasswordForm/>
        </AuthLayout>
    );
}