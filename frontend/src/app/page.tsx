import AppLayout from '@/components/layout/askpage/AppLayout';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function Home() {
  return (
    <ProtectedRoute>
      <AppLayout />;
    </ProtectedRoute>
  );
}