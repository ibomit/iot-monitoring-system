import {
    login as apiLogin,
    logout as apiLogout,
    getCurrentUser,
    refreshSession,
} from "@/api/api";
import { useState, useEffect, type ReactNode } from "react";
import { AuthContext } from "@/contexts/auth-context";
import type { IUser } from "@/api/types";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<IUser | null>(null);
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function restoreSession() {
        try {
            if ( await refreshSession()) {
                setUser(await getCurrentUser());
            }
        }
        catch {
            setUser(null);
        }
        finally {
            setLoading(false);
        }
    }
    restoreSession();
  }, []);

  async function login(username: string, password: string) {
    await apiLogin(username, password);
    setUser(await getCurrentUser());
  }

  async function logout() {
    await apiLogout();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
        {children}
    </AuthContext.Provider>
  )
}
