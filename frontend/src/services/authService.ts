import { api, tokenStorage } from "@/services/api";
import type { AuthResponse, LoginPayload, RegisterPayload, User } from "@/types/auth";

export const authService = {
  async register(payload: RegisterPayload): Promise<AuthResponse> {
    const { data } = await api.post<AuthResponse>("/auth/register", payload);
    tokenStorage.setTokens(data.tokens);
    return data;
  },

  async login(payload: LoginPayload): Promise<AuthResponse> {
    const { data } = await api.post<AuthResponse>("/auth/login", payload);
    tokenStorage.setTokens(data.tokens);
    return data;
  },

  async logout(): Promise<void> {
    try {
      await api.post("/auth/logout");
    } finally {
      tokenStorage.clear();
    }
  },

  async getCurrentUser(): Promise<User> {
    const { data } = await api.get<User>("/auth/me");
    return data;
  },

  async forgotPassword(email: string): Promise<void> {
    await api.post("/auth/forgot-password", { email });
  },

  async resetPassword(token: string, new_password: string): Promise<void> {
    await api.post("/auth/reset-password", { token, new_password });
  },
};
