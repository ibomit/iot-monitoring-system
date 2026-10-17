import { useMemo, useState } from 'react'
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from 'recharts'
import type { IMeasurement } from '../services/api'
import { formatMeasurement, formatUnit } from '@/lib/units'
import {
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
    type ChartConfig,
} from '@/components/ui/chart'

interface IChartPoint {
    time: number
    value: number
}

interface IMetricChartProps {
    points: IChartPoint[]
    label: string
    color: string
    compact: boolean
}

interface IMeasurementChartProps {
    data: IMeasurement[]
    compact: boolean
}

// How many points the small chart of one metric shows
const COMPACT_POINTS = 20

// The API returns measurements of all metrics mixed together, newest first.
// A chart needs one metric at a time, oldest first, as plain {time, value}.
function toPoints(data: IMeasurement[], metric: string): IChartPoint[] {
    return data
        .filter((measurement) => measurement.metric === metric)
        .map((measurement) => ({
            time: new Date(measurement.created_at).getTime(),
            value: measurement.value,
        }))
        .sort((a, b) => a.time - b.time)
}

function chartColor(index: number): string {
    return `var(--chart-${(index % 5) + 1})`
}

function MetricChart({ points, label, color, compact }: IMetricChartProps) {
    const config: ChartConfig = {
        value: { label, color },
    }

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
                    domain={['dataMin', 'dataMax']}
                    hide={compact}
                    tickLine={true}
                    axisLine={true}
                    tickMargin={8}
                    minTickGap={32}
                    tickFormatter={(value) =>
                        new Date(value).toLocaleTimeString([], {
                            hour: '2-digit',
                            minute: '2-digit',
                        })
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
                {/* {!compact && ( */}
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
                {/* )} */}
                <Line
                    dataKey="value"
                    type="monotone"
                    stroke="var(--color-value)"
                    strokeWidth={2}
                    dot={false}
                    isAnimationActive={false}
                />
            </LineChart>
        </ChartContainer>
    )
}

export function MeasurementChart({ data, compact }: IMeasurementChartProps) {
    const [selectedMetric, setSelectedMetric] = useState<string | null>(null)

    // Distinct metrics of this sensor, e.g. ["temperature", "humidity"]
    const metrics = useMemo(
        () => [...new Set(data.map((measurement) => measurement.metric))],
        [data]
    )

    // The newest measurement of every metric (shown on the tabs)
    const latestByMetric = useMemo(() => {
        const latest: Record<string, IMeasurement> = {}
        for (const measurement of data) {
            const current = latest[measurement.metric]
            if (
                current === undefined ||
                new Date(measurement.created_at) > new Date(current.created_at)
            ) {
                latest[measurement.metric] = measurement
            }
        }
        return latest
    }, [data])

    if (metrics.length === 0) {
        return <p className="sensor-card-empty">No measurements yet</p>
    }

    // Small card: one small chart per metric
    if (compact) {
        return (
            <div className="sensor-charts">
                {metrics.map((metric, index) => (
                    <div key={metric} className="sensor-chart-compact">
                        <span className="sensor-chart-label">
                            {metric} ({formatUnit(latestByMetric[metric].unit)})
                        </span>
                        <MetricChart
                            points={toPoints(data, metric).slice(-COMPACT_POINTS)}
                            label={metric}
                            color={chartColor(index)}
                            compact
                        />
                    </div>
                ))}
            </div>
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
                points={toPoints(data, activeMetric)}
                label={`${activeMetric} (${formatUnit(latestByMetric[activeMetric].unit)})`}
                color={chartColor(activeIndex)}
                compact={false}
            />
        </div>
    )
}

export default MeasurementChart
