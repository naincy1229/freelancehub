import { useAuth } from "@/contexts/AuthContext";

export default function DashboardPage() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 p-8 dark:bg-surface-dark">
      <div className="mx-auto max-w-4xl">
        <div className="card flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">Welcome, {user?.full_name} 👋</h1>
            <p className="mt-1 text-sm text-gray-500">
              Logged in as <span className="font-medium capitalize">{user?.role}</span> — {user?.email}
            </p>
          </div>
          <button onClick={() => logout()} className="btn-primary bg-gray-800 hover:bg-gray-900">
            Log out
          </button>
        </div>
        <div className="mt-6 rounded-xl border border-dashed border-gray-300 p-8 text-center text-sm text-gray-500 dark:border-gray-700">
          Project browsing, proposals, contracts, and wallet features land here in the next build steps.
        </div>
      </div>
    </div>
  );
}
