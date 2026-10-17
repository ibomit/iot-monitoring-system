import { useEffect, useState } from 'react'
import { Activity, ChevronDown } from 'lucide-react'
import {
    getSensorMeasurements,
    type IMeasurement,
    type ISensor,
} from '../services/api'
import { formatUnit, formatValue } from '@/lib/units'
import './SensorCard.css'
import MeasurementChart from './MeasurementChart'


interface ISensorCardProps {
    sensor: ISensor
}

// History points requested per metric (the API limit counts all metrics together)
const POINTS_PER_METRIC = 100
const MAX_LIMIT = 1000

// How often the graph asks for new measurements
const REFRESH_INTERVAL_MS = 5000

function SensorCard({
    sensor
}: ISensorCardProps) {

    const [expanded, setExpanded] = useState(false)
    const [history, setHistory] = useState<IMeasurement[]>([])
    const [historyLoading, setHistoryLoading] = useState(true)
    const [historyError, setHistoryError] = useState<string | null>(null)

    const metricCount = Math.max(sensor.latest_measurements.length, 1)
    const limit = Math.min(POINTS_PER_METRIC * metricCount, MAX_LIMIT)

    useEffect(() => {
        let cancelled = false
        let timeoutId: number | undefined

        async function loadHistory() {
            try {
                const data = await getSensorMeasurements(sensor.sensor_uid, limit)
                if (!cancelled) {
                    setHistory(data)
                    setHistoryError(null)
                }
            } catch {
                if (!cancelled) {
                    setHistoryError('Failed to load the measurement history')
                }
            } finally {
                if (!cancelled) {
                    setHistoryLoading(false)
                    // Schedule the next request only after this one finished,
                    // so a slow response never overlaps with the next request
                    timeoutId = window.setTimeout(loadHistory, REFRESH_INTERVAL_MS)
                }
            }
        }

        void loadHistory()
        return () => {
            cancelled = true
            window.clearTimeout(timeoutId)
        }
    }, [sensor.sensor_uid, limit])

    return (
        <div
            className={
                expanded
                    ? 'sensor-card sensor-card--expanded'
                    : 'sensor-card'
            }
        >
            <button
                type="button"
                className="sensor-card-header"
                aria-expanded={expanded}
                aria-label={`${expanded ? 'Collapse' : 'Expand'} ${sensor.name}`}
                onClick={() => setExpanded((current) => !current)}
            >
                <span className="sensor-card-icon">
                    <Activity aria-hidden="true" />
                </span>
                <span className="sensor-card-title">
                    <h3>{sensor.name}</h3>
                    <span>{sensor.sensor_uid}</span>
                </span>
                <span className="sensor-card-type">{sensor.sensor_type}</span>
                <ChevronDown className="sensor-card-chevron" aria-hidden="true" />
            </button>

            <section className="sensor-card-section">
                <h4>Latest measurements</h4>
                {sensor.latest_measurements.length > 0 ? (
                    <ul className="sensor-measurements">
                        {sensor.latest_measurements.map((measurement) => (
                            <li key={measurement.id}>
                                <span className="sensor-measurement-metric">
                                    {measurement.metric}
                                </span>
                                <span className="sensor-measurement-value">
                                    {formatValue(measurement.value)}
                                    <small> {formatUnit(measurement.unit)}</small>
                                </span>
                                <time
                                    className="sensor-measurement-time"
                                    dateTime={measurement.created_at}
                                >
                                    {new Date(measurement.created_at).toLocaleString()}
                                </time>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="sensor-card-empty">No measurements yet</p>
                )}
            </section>

            <section className="sensor-card-section">
                <h4>Measurement graph</h4>
                {historyLoading && (
                    <p className="sensor-card-empty">Loading graph...</p>
                )}
                {historyError && <p role="alert">{historyError}</p>}
                {/* Keep showing the last data if a refresh fails */}
                {!historyLoading && (history.length > 0 || !historyError) && (
                    <MeasurementChart data={history} compact={!expanded} />
                )}
            </section>
        </div>
    )
}
export default SensorCard
