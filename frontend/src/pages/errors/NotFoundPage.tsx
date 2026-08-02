import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-4 text-center dark:bg-surface-dark">
      <h1 className="text-6xl font-extrabold text-primary-600">404</h1>
      <p className="mt-3 text-lg font-medium">Page not found</p>
      <p className="mt-1 text-sm text-gray-500">The page you're looking for doesn't exist or has moved.</p>
      <Link to="/" className="btn-primary mt-6">
        Back to home
      </Link>
    </div>
  );
}
