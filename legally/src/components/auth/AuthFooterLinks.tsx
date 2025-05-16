import Link from "next/link";

// type must be exactly one of these three strings. Nothing else is allowed.
export default function AuthFooterLinks({ type }: { type: "login" | "register" | "forgot" }) {
    return (
  <div className="mt-4 text-sm text-center text-gray-600">
    {type === "login" && (
      <>
        Don’t have an account?{" "}
        <Link href="/auth/register" className="text-blue-600 hover:underline">
          Register
        </Link>
        {"  "} | {"  "}
        <Link href="/auth/forgot" className="text-blue-600 hover:underline">
          Forgot Password
        </Link>
      </>
    )}

    {type === "register" && (
      <>
        Already have an account?{" "}
        <Link href="/auth/login" className="text-blue-600 hover:underline">
          Login
        </Link>
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