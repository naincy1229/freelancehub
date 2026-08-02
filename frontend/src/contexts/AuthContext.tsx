import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { authService } from "@/services/authService";
import { tokenStorage } from "@/services/api";
import type { LoginPayload, RegisterPayload, User } from "@/types/auth";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (payload: LoginPayload) => Promise<User>;
  register: (payload: RegisterPayload) => Promise<User>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function bootstrap() {
      const hasToken = Boolean(tokenStorage.getAccessToken());
      if (!hasToken) {
        setIsLoading(false);
        return;
      }
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch {
        tokenStorage.clear();
      } finally {
        setIsLoading(false);
      }
    }
    bootstrap();
  }, []);

  async function login(payload: LoginPayload): Promise<User> {
    const { user: loggedInUser } = await authService.login(payload);
    setUser(loggedInUser);
    return loggedInUser;
  }

  async function register(payload: RegisterPayload): Promise<User> {
    const { user: newUser } = await authService.register(payload);
    setUser(newUser);
    return newUser;
  }

  async function logout(): Promise<void> {
    await authService.logout();
    setUser(null);
  }

  return (
    <AuthContext.Provider
      value={{ user, isLoading, isAuthenticated: Boolean(user), login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
