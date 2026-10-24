// Time ranges of the sensor charts. 
export const RANGES = {
    '1m' : { ms: 1 * 60 * 1000},
    '5m' : { ms: 5 * 60 * 1000 },
    '15m': { ms: 15 * 60 * 1000 },
    '1h': { ms: 60 * 60 * 1000 },
    '24h': { ms: 24 * 60 * 60 * 1000 },
    '7d': { ms: 7 * 24 * 60 * 60 * 1000 },
    '30d': { ms: 30 * 24 * 60 * 60 * 1000 },
} as const

export type RangeKey = keyof typeof RANGES

export const RANGE_KEYS = Object.keys(RANGES) as RangeKey[]

// Points per metric the charts ask the API for
export const MAX_POINTS = 300

// Width of one bucket in milliseconds. This is the same formula as the backend
// (the range divided by max_points, rounded up to whole seconds, at least 1 second),
// so the chart knows how far apart the points are.
export function getBucketMs(rangeMs: number): number {
    return Math.max(1, Math.ceil(rangeMs / 1000 / MAX_POINTS)) * 1000
}
