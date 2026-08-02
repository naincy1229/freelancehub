import { z } from "zod";

const passwordRule = z
  .string()
  .min(8, "Password must be at least 8 characters")
  .max(72, "Password is too long")
  .refine((v) => /[A-Z]/.test(v), "Password must contain at least one uppercase letter")
  .refine((v) => /[0-9]/.test(v), "Password must contain at least one digit");

export const registerSchema = z
  .object({
    full_name: z.string().min(2, "Name must be at least 2 characters").max(150),
    email: z.string().email("Enter a valid email address"),
    password: passwordRule,
    confirm_password: z.string(),
    role: z.enum(["client", "freelancer"], { required_error: "Select a role" }),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  });

export type RegisterFormValues = z.infer<typeof registerSchema>;

export const loginSchema = z.object({
  email: z.string().email("Enter a valid email address"),
  password: z.string().min(1, "Password is required"),
});

export type LoginFormValues = z.infer<typeof loginSchema>;

export const forgotPasswordSchema = z.object({
  email: z.string().email("Enter a valid email address"),
});

export type ForgotPasswordFormValues = z.infer<typeof forgotPasswordSchema>;
