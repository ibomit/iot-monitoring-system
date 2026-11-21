import { createContext } from "react";
import type { IUser } from "@/api/types";

export interface IAuthContext {
    user: IUser | null;
    loading: boolean;
    login: (username: string, password: string ) => Promise<void>;
    logout: () => Promise<void>;
}

export const AuthContext = createContext<IAuthContext | null >(null);