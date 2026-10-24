import { useEffect, useState } from 'react'
import { ArrowLeft, Clock, Cpu, MapPin } from 'lucide-react'
import { Button } from "@/components/ui/button"
import {
  getDeviceDashboard,
  type IDeviceDashboard,
} from '../services/api'
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group"
import { RANGE_KEYS, type RangeKey } from '@/lib/ranges'

import { useNavigate, useParams } from 'react-router-dom'
import SensorCard from '../components/SensorCard'
import './DeviceDashboardPage.css'
// interface DeviceDashboardProps {
//   device: Device
//   // onBack: () => void
// }

// How often the status, last seen time and latest values are refreshed
const DASHBOARD_REFRESH_INTERVAL_MS = 5000

function DeviceDashboard() {

  const [dashboard, setDashboard] = useState<IDeviceDashboard | null>(null)
  const [range, setRange] = useState<RangeKey>('1h')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const navigate = useNavigate()
  const { deviceUid } = useParams()

  useEffect(() => {
    if (!deviceUid) {
      return
    }

    let cancelled = false
    let timeoutId: number | undefined

    async function loadDashboard(uid: string, isFirstLoad: boolean) {
      // Only the first load shows the loading state, refreshes happen silently
      if (isFirstLoad) {
        setLoading(true)
        setError(null)
      }
      let notFound = false
      try {
        const data = await getDeviceDashboard(uid)
        if (cancelled) {
          return
        }
        setDashboard(data)
        if (data === null) {
          notFound = true
          setError('Device not found')
        } else {
          setError(null)
        }
      } catch {
        if (!cancelled) {
          setError('Failed to load device dashboard')
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
          // Schedule the next refresh after this request finished, so requests
          // never overlap. A device that does not exist is not polled.
          if (!notFound) {
            timeoutId = window.setTimeout(
              () => void loadDashboard(uid, false),
              DASHBOARD_REFRESH_INTERVAL_MS
            )
          }
        }
      }
    }

    void loadDashboard(deviceUid, true)
    return () => {
      cancelled = true
      window.clearTimeout(timeoutId)
    }
  }, [deviceUid])

  return (
    <main className="dashboard-page">
      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={() => navigate('/devices')}>
        <ArrowLeft aria-hidden="true" />
        Back to devices
      </Button>

      {loading && <p className="dashboard-state">Loading dashboard...</p>}

      {error && (
        <p role="alert" className="dashboard-state dashboard-state--error">
          {error}
        </p>
      )}

      {!loading && dashboard && (
        <>
          <header className="dashboard-hero">
            <div>
              <p className="dashboard-eyebrow">Device dashboard</p>
              <h1>{dashboard.name}</h1>
              <p className="dashboard-uid">{dashboard.device_uid}</p>
            </div>
            <span className={`dashboard-status status-${dashboard.status}`}>
              <span /> {dashboard.status}
            </span>
          </header>

          <div className="dashboard-info">
            <div className="dashboard-info-card">
              <MapPin aria-hidden="true" />
              <div>
                <span>Location</span>
                <strong>{dashboard.location}</strong>
              </div>
            </div>
            <div className="dashboard-info-card">
              <Clock aria-hidden="true" />
              <div>
                <span>Last seen</span>
                <strong>
                  {dashboard.last_seen_at
                    ? new Date(dashboard.last_seen_at).toLocaleString()
                    : 'Never'}
                </strong>
              </div>
            </div>
            <div className="dashboard-info-card">
              <Cpu aria-hidden="true" />
              <div>
                <span>Sensors</span>
                <strong>{dashboard.sensors.length}</strong>
              </div>

            </div>
          </div>

          <section className="dashboard-sensors">
            <div className="dashboard-sensors-header">
              <h2>Sensors</h2>
              <ToggleGroup
                variant="outline"
                aria-label="Time range"
                value={[range]}
                onValueChange={(value) => {
                  // Clicking the active button reports an empty selection: ignore it
                  if (value.length > 0) {
                    setRange(value[0] as RangeKey)
                  }
                }}
              >
                {RANGE_KEYS.map((option) => (
                  <ToggleGroupItem key={option} value={option}>
                    {option}
                  </ToggleGroupItem>
                ))}
              </ToggleGroup>
            </div>
            {dashboard.sensors.length > 0 ? (
              <div className="dashboard-sensor-grid">
                {dashboard.sensors.map(
                  (sensor) => (
                    <SensorCard
                      key={sensor.sensor_uid}
                      sensor={sensor}
                      range={range} />
                  )
                )}
              </div>
            ) : (
              <p className="dashboard-state">
                No sensors yet. They appear once the device registers them.
              </p>
            )}
          </section>
        </>
      )}
    </main>
  )
}

export default DeviceDashboard