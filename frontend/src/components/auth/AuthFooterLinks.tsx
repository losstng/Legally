import Link from "next/link";

export default function AuthFooterLinks({ type }: { type: "login" | "register" | "forgot" }) {
    return (
        <div className="text-sm text-center mt-4 text-gray-600">
            {type === "login" && (
                <>
                    Don't Have an account?{" "}
                    <link href="/auth/register" className="text-blue-600 hover:underline">
                        Register
                    </link>{" "}
                    | {" "}
                    <Link href="/auth/forgot" className="text-blue-600 hover:underline">
                        Forgot Password
                    </Link>
                </>
            )}
            {type === "register" && (
                <>
                    Already have an account?{" "}
                    <link href="/auth/login" className="text-blue-600 hover:underline">
                        Login
                    </link>
                </>
            )}
            {type === "forgot" && (
                <>
                    Remembered?{" "}
                    <Link href="/auth/login" className="text-blue-600 hover:underline">
                        Back to Login
                    </Link>
                </>
            )}
        </div>
    );
}