import { useMemo, useState } from 'react'
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts'
import type { IMeasurement, IMeasurementBucket } from '../services/api'
import { formatMeasurement, formatUnit } from '@/lib/units'
import { getBucketMs } from '@/lib/ranges'
import {
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    type ChartConfig,
} from '@/components/ui/chart'


// A null value is a gap: the line is not drawn through it
interface IChartPoint {
    time: number
    value: number | null
}

interface IMetricChartProps {
    points: IChartPoint[]
    label: string
    color: string
    start: number
    end: number
    compact: boolean
}

interface IMeasurementChartProps {
    data: IMeasurementBucket[]
    // The latest value of every metric of the sensor (tabs, units, metric list)
    latest: IMeasurement[]
    // The time window of the data, in milliseconds
    start: number
    end: number
    compact: boolean
}

const DAY_MS = 24 * 60 * 60 * 1000

// The shortest time without data that counts as a gap. Readings never arrive
// exactly on time, so with narrow buckets (about the sending interval) an
// occasional empty bucket is normal and must not break the line.
const MIN_GAP_MS = 30 * 1000

// The buckets of all metrics come mixed together. A chart needs one metric at a
// time, oldest first, as plain {time, value}. The API leaves out buckets without
// readings, so a long jump between two buckets is a gap: a null point is inserted
// there so the line breaks instead of joining the two points.
function toPoints(
    data: IMeasurementBucket[],
    metric: string,
    bucketMs: number
): IChartPoint[] {
    const buckets = data
        .filter((bucket) => bucket.metric === metric)
        .map((bucket) => ({
            time: new Date(bucket.bucket_start).getTime(),
            value: bucket.value,
        }))
        .sort((a, b) => a.time - b.time)

    // Three missing buckets, but at least MIN_GAP_MS
    const gapMs = Math.max(bucketMs * 3, MIN_GAP_MS)

    const points: IChartPoint[] = []
    buckets.forEach((bucket, index) => {
        const previous = buckets[index - 1]
        if (previous !== undefined && bucket.time - previous.time > gapMs) {
            points.push({ time: previous.time + bucketMs, value: null })
        }
        points.push(bucket)
    })
    return points
}

function chartColor(index: number): string {
    return `var(--chart-${(index % 5) + 1})`
}

function MetricChart({ points, label, color, start, end, compact }: IMetricChartProps) {
    const config: ChartConfig = {
        value: { label, color },
    }

    // Ranges of a day or more need the weekday on the ticks, shorter ones only the time
    const tickOptions: Intl.DateTimeFormatOptions =
        end - start >= DAY_MS
            ? { weekday: 'short', hour: '2-digit', minute: '2-digit' }
            : { hour: '2-digit', minute: '2-digit' }

    return (
        <ChartContainer
            config={config}
            className={compact ? 'aspect-auto h-[70px] w-full' : 'aspect-auto h-[300px] w-full'}
        >
            <LineChart
                accessibilityLayer
                data={points}
                margin={compact ? { top: 4, right: 4, bottom: 4, left: 4 } : { left: 12, right: 12 }}
            >
                {!compact && <CartesianGrid vertical={false} />}
                <XAxis
                    height={50}
                    label={{
                        value: 'Time',
                        position: 'insideBottom',
                        offset: 0,
                        fill: 'var(--muted-foreground)',
                    }}
                    dataKey="time"
                    type="number"
                    scale="time"
                    // The selected window, so time without data stays empty
                    domain={[start, end]}
                    hide={compact}
                    tickLine={true}
                    axisLine={true}
                    tickMargin={8}
                    minTickGap={32}
                    tickFormatter={(value) =>
                        new Date(value).toLocaleString([], tickOptions)
                    }
                />
                <YAxis
                    label={{
                        value: label,
                        angle: -90,
                        position: 'insideLeft',
                        style: { textAnchor: 'middle' },
                        fill: 'var(--muted-foreground)',
                    }}
                    hide={compact}
                    width={64}
                    tickLine={true}
                    axisLine={true}
                    domain={['auto', 'auto']}
                />
                <ChartTooltip
                    content={
                        <ChartTooltipContent
                            // The first argument is the config label, not the X value:
                            // read the timestamp from the data point instead
                            labelFormatter={(_, payload) =>
                                new Date(payload[0].payload.time).toLocaleString()
                            }
                        />
                    }
                />
                <Line
                    dataKey="value"
                    type="monotone"
                    stroke="var(--color-value)"
                    strokeWidth={2}
                    // Few points: draw them, so a single reading between two gaps is visible
                    dot={!compact && points.length <= 30}
                    connectNulls={false}
                    isAnimationActive={false}
                />
            </LineChart>

        </ChartContainer>
    )
}

export function MeasurementChart({
    data,
    latest,
    start,
    end,
    compact,
}: IMeasurementChartProps) {
    const [selectedMetric, setSelectedMetric] = useState<string | null>(null)

    const bucketMs = getBucketMs(end - start)

    // The latest value of every metric of the sensor. The metrics (and so the tabs)
    // come from here and not from the buckets, so they stay the same when a range
    // has no data for a metric.
    const latestByMetric = useMemo(
        () => Object.fromEntries(latest.map((measurement) => [measurement.metric, measurement])),
        [latest]
    )
    const metrics = Object.keys(latestByMetric)

    if (metrics.length === 0) {
        return <p className="sensor-card-empty">No measurements yet</p>
    }

    if (data.length === 0) {
        return <p className="sensor-card-empty">No measurements in this range</p>
    }

    // Small card: one small chart per metric
    if (compact) {
        return (
            <>
                <div className="sensor-charts">
                    {metrics.map((metric, index) => (
                        <div key={metric} className="sensor-chart-compact">
                            <span className="sensor-chart-label">
                                {metric} ({formatUnit(latestByMetric[metric].unit)})
                            </span>

                            <MetricChart
                                points={toPoints(data, metric, bucketMs)}
                                label={metric}
                                color={chartColor(index)}
                                start={start}
                                end={end}
                                compact
                            />
                        </div>
                    ))}
                </div>
            </>
        )
    }

    // Expanded card: tabs to pick a metric, one large chart
    const activeMetric =
        selectedMetric !== null && metrics.includes(selectedMetric)
            ? selectedMetric
            : metrics[0]
    const activeIndex = metrics.indexOf(activeMetric)

    return (
        <div>
            <div className="sensor-chart-tabs" role="tablist">
                {metrics.map((metric) => (
                    <button
                        key={metric}
                        type="button"
                        role="tab"
                        aria-selected={metric === activeMetric}
                        className="sensor-chart-tab"
                        onClick={() => setSelectedMetric(metric)}
                    >
                        <span>{metric}</span>
                        <strong>
                            {formatMeasurement(latestByMetric[metric].value, latestByMetric[metric].unit)}
                        </strong>
                    </button>
                ))}
            </div>
            <MetricChart
                points={toPoints(data, activeMetric, bucketMs)}
                label={`${activeMetric} (${formatUnit(latestByMetric[activeMetric].unit)})`}
                color={chartColor(activeIndex)}
                start={start}
                end={end}
                compact={false}
            />
        </div>
    )
}

export default MeasurementChart
