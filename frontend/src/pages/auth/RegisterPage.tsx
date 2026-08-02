import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2, Briefcase, Check } from "lucide-react";

import { useAuth } from "@/contexts/AuthContext";
import { registerSchema, type RegisterFormValues } from "@/schemas/auth";
import { extractApiErrorMessage, cn } from "@/utils/cn";

export default function RegisterPage() {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: { role: "freelancer" },
  });

  const selectedRole = watch("role");

  async function onSubmit(values: RegisterFormValues) {
    setServerError(null);
    try {
      await registerUser({
        email: values.email,
        password: values.password,
        full_name: values.full_name,
        role: values.role,
      });
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setServerError(extractApiErrorMessage(err));
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-10 dark:bg-surface-dark">
      <div className="w-full max-w-md">
        <div className="mb-8 flex flex-col items-center">
          <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl bg-primary-600 text-white">
            <Briefcase size={24} />
          </div>
          <h1 className="text-2xl font-bold">Create your account</h1>
          <p className="mt-1 text-sm text-gray-500">Join FreelanceHub as a client or freelancer</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="card space-y-4" noValidate>
          {serverError && (
            <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-950 dark:text-red-300">
              {serverError}
            </div>
          )}

          <div>
            <label className="mb-1.5 block text-sm font-medium">I want to</label>
            <div className="grid grid-cols-2 gap-3">
              {(["freelancer", "client"] as const).map((roleOption) => (
                <button
                  key={roleOption}
                  type="button"
                  onClick={() => setValue("role", roleOption, { shouldValidate: true })}
                  className={cn(
                    "relative rounded-lg border px-4 py-3 text-left text-sm font-medium transition-colors",
                    selectedRole === roleOption
                      ? "border-primary-600 bg-primary-50 text-primary-700 dark:bg-primary-900/20"
                      : "border-gray-300 text-gray-700 hover:border-gray-400 dark:border-gray-700 dark:text-gray-300"
                  )}
                >
                  {roleOption === "freelancer" ? "Find work" : "Hire talent"}
                  {selectedRole === roleOption && (
                    <Check size={16} className="absolute right-3 top-3 text-primary-600" />
                  )}
                </button>
              ))}
            </div>
            {errors.role && <p className="mt-1 text-xs text-red-600">{errors.role.message}</p>}
          </div>

          <div>
            <label htmlFor="full_name" className="mb-1.5 block text-sm font-medium">
              Full name
            </label>
            <input
              id="full_name"
              type="text"
              autoComplete="name"
              className="input-field"
              placeholder="Naincy Shukla"
              {...register("full_name")}
            />
            {errors.full_name && <p className="mt-1 text-xs text-red-600">{errors.full_name.message}</p>}
          </div>

          <div>
            <label htmlFor="email" className="mb-1.5 block text-sm font-medium">
              Email
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              className="input-field"
              placeholder="you@example.com"
              {...register("email")}
            />
            {errors.email && <p className="mt-1 text-xs text-red-600">{errors.email.message}</p>}
          </div>

          <div>
            <label htmlFor="password" className="mb-1.5 block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              type="password"
              autoComplete="new-password"
              className="input-field"
              placeholder="At least 8 characters"
              {...register("password")}
            />
            {errors.password && <p className="mt-1 text-xs text-red-600">{errors.password.message}</p>}
          </div>

          <div>
            <label htmlFor="confirm_password" className="mb-1.5 block text-sm font-medium">
              Confirm password
            </label>
            <input
              id="confirm_password"
              type="password"
              autoComplete="new-password"
              className="input-field"
              placeholder="Re-enter your password"
              {...register("confirm_password")}
            />
            {errors.confirm_password && (
              <p className="mt-1 text-xs text-red-600">{errors.confirm_password.message}</p>
            )}
          </div>

          <button type="submit" disabled={isSubmitting} className="btn-primary w-full">
            {isSubmitting ? <Loader2 className="animate-spin" size={18} /> : "Create Account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-500">
          Already have an account?{" "}
          <Link to="/login" className="font-semibold text-primary-600 hover:text-primary-700">
            Log in
          </Link>
        </p>
      </div>
    </div>
  );
}
