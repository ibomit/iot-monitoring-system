import './App.css'
import NavBar from './components/NavBar'
import Devices from './pages/DevicesPage'
import DeviceDashboard from './pages/DeviceDashboardPage'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/HomePage'

function App() {
    return (
        <>
            <div>
                <NavBar />
                <main className="main-content">
                    <Routes>
                        <Route path="/" element={<Home />}>Hello</Route>
                        <Route path="/devices" element={<Devices />}/>
                        <Route 
                        path="/devices/:deviceUid"
                        element={<DeviceDashboard />} />
                    </Routes>
                </main>
            </div>
        </>
    )
}

export default App