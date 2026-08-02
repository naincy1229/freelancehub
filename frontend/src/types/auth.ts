export type UserRole = "client" | "freelancer" | "admin";
export type AuthProvider = "local" | "google";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  auth_provider: AuthProvider;
  is_active: boolean;
  is_email_verified: boolean;
  is_profile_completed: boolean;
  created_at: string;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface AuthResponse {
  user: User;
  tokens: TokenPair;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  role: Exclude<UserRole, "admin">;
}

export interface LoginPayload {
  email: string;
  password: string;
}

/** Shape of FastAPI's error responses, used to surface backend validation messages. */
export interface ApiErrorResponse {
  detail:
    | string
    | { msg: string; loc: (string | number)[]; type: string }[];
}
