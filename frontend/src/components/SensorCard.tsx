import { useEffect, useState } from 'react'
import { Activity, ChevronDown } from 'lucide-react'
import {
    getSensorMeasurementBuckets,
    type IMeasurementBucket,
    type ISensor,
} from '../services/api'
import { formatUnit, formatValue } from '@/lib/units'
import { MAX_POINTS, RANGES, type RangeKey } from '@/lib/ranges'
import './SensorCard.css'
import MeasurementChart from './MeasurementChart'


interface ISensorCardProps {
    sensor: ISensor
    range: RangeKey
}

// The fetched buckets together with the time window they belong to
interface IChartData {
    buckets: IMeasurementBucket[]
    start: number
    end: number
}

// How often the graph asks for new measurements
const REFRESH_INTERVAL_MS = 5000

function SensorCard({
    sensor,
    range
}: ISensorCardProps) {

    const [expanded, setExpanded] = useState(false)
    const [chartData, setChartData] = useState<IChartData | null>(null)
    const [historyLoading, setHistoryLoading] = useState(true)
    const [historyError, setHistoryError] = useState<string | null>(null)

    useEffect(() => {
        let cancelled = false
        let timeoutId: number | undefined

        async function loadBuckets(isFirstLoad: boolean) {
            // A new range shows the loading state, not the graph of the old range
            if (isFirstLoad) {
                setHistoryLoading(true)
                setHistoryError(null)
                setChartData(null)
            }
            try {
                // The window moves forward on every refresh, so it is computed here
                const end = new Date()
                const start = new Date(end.getTime() - RANGES[range].ms)
                const buckets = await getSensorMeasurementBuckets(
                    sensor.sensor_uid,
                    start.toISOString(),
                    end.toISOString(),
                    MAX_POINTS
                )
                if (!cancelled) {
                    setChartData({
                        buckets,
                        start: start.getTime(),
                        end: end.getTime(),
                    })
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
                    timeoutId = window.setTimeout(
                        () => void loadBuckets(false),
                        REFRESH_INTERVAL_MS
                    )
                }
            }
        }

        void loadBuckets(true)
        return () => {
            cancelled = true
            window.clearTimeout(timeoutId)
        }
    }, [sensor.sensor_uid, range])

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
                {!historyLoading && chartData !== null && (
                    <MeasurementChart
                        data={chartData.buckets}
                        latest={sensor.latest_measurements}
                        start={chartData.start}
                        end={chartData.end}
                        compact={!expanded}
                    />
                )}
            </section>
        </div>
    )
}
export default SensorCard
