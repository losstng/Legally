import AppLayout from '@/layout/askpage/AppLayout';
import TokenGate from '@/utils/TokenGate';
import ProtectedRoute from '@/utils/ProtectedRoute';
import './globals.css';

export default function Home() {
  return (
        <AppLayout activeSessionId={null} />
  );
}