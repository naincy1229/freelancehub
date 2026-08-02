import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Extracts a human-readable message from a FastAPI error response. */
export function extractApiErrorMessage(error: unknown): string {
  const anyErr = error as { response?: { data?: { detail?: unknown } } };
  const detail = anyErr?.response?.data?.detail;

  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((d) => d.msg).join(", ");
  }
  return "Something went wrong. Please try again.";
}
