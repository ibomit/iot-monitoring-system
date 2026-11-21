import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/hooks/use-auth";
import { Skeleton } from "@/components/ui/skeleton";

export function ProtectedRoute() {
    const { user, loading } = useAuth()
    const location = useLocation(); 
    
    if (loading) return <Skeleton className="h-svh w-full" />;
    
    if (!user) return <Navigate to="/login" state={{ from: location }} replace />;

    return <Outlet />; 
}