import { useEffect, useState } from 'react'
import {Button} from "@/components/ui/button"
import {
  getDeviceDashboard,
  type IDeviceDashboard,
} from '../services/api'

import { useNavigate, useParams } from 'react-router-dom'
import SensorCard from '../components/SensorCard'
import './DeviceDashboardPage.css'
// interface DeviceDashboardProps {
//   device: Device
//   // onBack: () => void
// }

function DeviceDashboard() {

  const [dashboard, setDashboard] = useState<IDeviceDashboard | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { deviceUid } = useParams()

  useEffect(() => {
    if (!deviceUid) {
      return
    }

    let cancelled = false

    async function loadDashboard(uid: string) {
      setLoading(true)
      setError(null)
      try {
        const data = await getDeviceDashboard(uid)
        if (cancelled) {
          return
        }
        setDashboard(data)
        if (data === null) {
          setError('Device not found')
        }
      } catch {
        if (!cancelled) {
          setError('Failed to load device dashboard')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    void loadDashboard(deviceUid)
    return () => {
      cancelled = true
    }
  }, [deviceUid])

  return (
    <main className="main">
      <Button
        type="button"
        onClick={() => navigate('/devices')}>
        ← Back to devices
      </Button>

      {loading && <p>Loading dashboard...</p>}

      {error && <p role="alert">{error}</p>}

      {!loading && dashboard && (
        <section>
          <div className="dashboard-grid">
            <div className="dashboard-device-information">

              <h2>{dashboard.name}</h2>
              <p>
                <strong>Device:</strong> {dashboard.device_uid}
              </p>
              <p>
                <strong>Location:</strong> {dashboard.location}
              </p>
              <p>
                <strong>Status:</strong> {dashboard.status}
              </p>
              <p> {/*TODO: Add "registered_at" */}
                <strong>Registered:</strong>
              </p>
            </div>
            <div className="dashboard-sensors">
              <h2>Sensors</h2>
              <div className='devices-grid'>
                {dashboard.sensors.map(
                  (sensor) => (
                    <SensorCard
                      key={sensor.sensor_uid}
                      sensor={sensor} />
                  )
                )}
              </div>
            </div>
          </div>
        </section>
      )}
    </main>
  )
}

export default DeviceDashboard