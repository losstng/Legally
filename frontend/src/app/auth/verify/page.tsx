import VerifyOTPForm from "@/components/auth/VerifyOTPForm";
import AuthLayout from "@/components/layout/authpage/AuthLayout";

export default function VerifyPage() {
    return (
        <AuthLayout>
            <VerifyOTPForm/>
        </AuthLayout>
    );
}