import './App.css'
// import NavBar from './components/NavBar'
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"

import Devices from './pages/DevicesPage'
import DeviceDashboard from './pages/DeviceDashboardPage'
import { Navigate, Routes, Route } from 'react-router-dom'
import { Toaster } from './components/ui/toast'

function App() {
  return (
    <SidebarProvider>
      <AppSidebar />

      <SidebarInset>
        <header className="flex h-14 shrink-0 items-center gap-2 border-b bg-background/80 px-4 backdrop-blur md:px-6">
          <SidebarTrigger />
          <div className="h-5 w-px bg-border" />
          <span className="text-sm font-medium text-muted-foreground">Operations</span>
        </header>

        <div className="flex-1 bg-muted/20 p-4 md:p-6">
          <Routes>
            <Route path="/" element={<Navigate to="/devices" replace />} />
            <Route path="/devices" element={<Devices />} />
            <Route path="/devices/:deviceUid" element={<DeviceDashboard />} />
          </Routes>
        </div>
      </SidebarInset>

      <Toaster />
    </SidebarProvider>
  )
}

export default App