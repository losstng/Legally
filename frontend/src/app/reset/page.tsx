import ResetPasswordForm from "@/components/auth/ResetPasswordForm";
import AuthLayout from "@/components/layout/authpage/AuthLayout";

export default function ResetPage() {
    return(
        <AuthLayout>
            <ResetPasswordForm />
        </AuthLayout>
    );
}