import "./App.css";

import Devices from "./pages/DevicesPage";
import DeviceDashboard from "./pages/DeviceDashboardPage";
import Login from "./pages/LoginPage";
import { Navigate, Routes, Route } from "react-router-dom";
import { Toaster } from "./components/ui/toast";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { AppLayout } from "./components/AppLayout";

function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/" element={<Navigate to="/devices" replace />} />
            <Route path="/devices" element={<Devices />} />
            <Route path="/devices/:deviceUid" element={<DeviceDashboard />} />
          </Route>
        </Route>
      </Routes>
      <Toaster />
    </>
  );
}

export default App;
