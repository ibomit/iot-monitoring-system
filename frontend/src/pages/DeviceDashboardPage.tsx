import { useEffect, useState } from 'react'
import {
  getDeviceDashboard,
  type Device,
} from '../api/api'

interface DeviceDashboardProps {
  device: Device
  onBack: () => void
}

function DeviceDashboard({
  device,
  onBack,
}: DeviceDashboardProps) {
  const [dashboard, setDashboard] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadDashboard() {
      try {
        const data = await getDeviceDashboard(
          device.device_uid,
        )

        setDashboard(data)
      } catch {
        setError('Failed to load device dashboard')
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [device.device_uid])

  return (
    <main className="main">
      <button type="button" onClick={onBack}>
        ← Back to devices
      </button>

      <section>
        <h2>{device.name}</h2>

        <p>
          <strong>Device:</strong> {device.device_uid}
        </p>

        <p>
          <strong>Location:</strong> {device.location}
        </p>
      </section>

      {loading && <p>Loading dashboard...</p>}

      {error && <p>{error}</p>}

      {dashboard && (
        <section>
          <h2>Dashboard Data</h2>

          <pre>
            {JSON.stringify(dashboard, null, 2) ?? ''}
          </pre>
        </section>
      )}
    </main>
  )
}

export default DeviceDashboard