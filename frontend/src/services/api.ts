export interface IDevice {
    id: number
    device_uid: string
    name: string
    location: string
    created_at: string
    last_seen_at: string | null
    status: DeviceStatus
}

export type DeviceStatus = 'online' | 'offline' | 'unknown'
export interface ISensor {
    sensor_uid: string
    name: string
    sensor_type: string
    latest_measurements: IMeasurement[]
}
export interface IMeasurement {
    id: number
    sensor_id: number
    metric: string
    value: number
    unit: string
    created_at: string
}
export interface IDeviceDashboard {
    device_uid: string
    name: string
    location: string
    last_seen_at: string | null
    status: DeviceStatus
    sensors: ISensor[]
}
export interface DeviceDeleteResponse {
    success: boolean
    message: string
}

const API_BASE_URL: string = (
    import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
).replace(/\/$/, '')

export function getApiBaseUrl(): string {
    return API_BASE_URL
}

export async function checkApiHealth(): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            cache: 'no-store',
        })
        return response.ok
    } catch {
        return false
    }
}

export async function getDevices(): Promise<IDevice[]> {
    const response = await fetch(`${API_BASE_URL}/api/devices`)
    if (!response.ok) {
        throw new Error('Failed to fetch devices')
    }

    return response.json()
}

export async function createDevice(
    device_name: string,
    device_uid: string,
    device_location: string
): Promise<IDevice> {
    const response = await fetch(`${API_BASE_URL}/api/devices`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: device_name,
            device_uid: device_uid,
            location: device_location
        })
    })

    if (!response.ok) {
        const errorData = await response.json()
        const error = new Error(errorData.detail ?? "Failed to create device") as Error & {
            status: number
        }
        error.status = response.status
        throw error
    }
    return response.json()
}

export async function deleteDevice(
    deviceUid: string
): Promise<DeviceDeleteResponse> {
    const response = await fetch(
        `${API_BASE_URL}/api/devices/${deviceUid}`,
        {
            method: 'DELETE'
        }
    )

    if (!response.ok) {
        throw new Error(`Failed to delete device: ${deviceUid}`)
    }

    return response.json()
}

export async function getDevice(
    deviceUid: string
): Promise<IDevice | null> {

    const response = await fetch(
        `${API_BASE_URL}/api/devices/${deviceUid}`
    )
    if (response.status === 404) {
        return null
    }
    if (!response.ok) {
        throw new Error(`Failed to fetch device: ${deviceUid}`)
    }

    return response.json()
}

export async function getDeviceDashboard(
    deviceUid: string
): Promise<IDeviceDashboard | null> {
    const response = await fetch(`${API_BASE_URL}/api/devices/${deviceUid}/dashboard`)

    if (response.status === 404) {
        return null
    }
    if (!response.ok) {
        throw new Error('Failed to fetch device dashboard')
    }
    return response.json()


}




