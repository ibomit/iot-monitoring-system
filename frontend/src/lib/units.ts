// Units are stored as the devices send them ("celsius", "percent", "cm").
// These helpers only change how they are displayed.

const UNIT_SYMBOLS: Record<string, string> = {
    celsius: '°C',
    fahrenheit: '°F',
    percent: '%',
    cm: 'cm',
}

const numberFormat = new Intl.NumberFormat(undefined, {
    maximumFractionDigits: 1,
})

// Unknown units are shown as they are, so a new sensor never breaks the page
export function formatUnit(unit: string): string {
    return UNIT_SYMBOLS[unit] ?? unit
}

export function formatValue(value: number): string {
    return numberFormat.format(value)
}

export function formatMeasurement(value: number, unit: string): string {
    return `${formatValue(value)} ${formatUnit(unit)}`
}
