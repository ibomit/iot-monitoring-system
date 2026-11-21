/** Returns the auth state and actions (user, loading, login, logout). Must be used inside <AuthProvider>. */

import { useContext } from "react"
import { AuthContext } from "@/contexts/auth-context";

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === null) {
        throw new Error("useAuth must be used inside AuthProvider")
    }
    return context
}

