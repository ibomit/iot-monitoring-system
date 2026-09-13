export interface IDevice {
    id: number
    device_uid: string
    name: string
    location: string
    created_at: string
}
export interface ISensor{
    sensor_uid: string
    name: string
    sensor_type: string
    latest_measurements: IMeasurement[]
}
export interface IMeasurement{
    id: number
    sensor_id: number
    metric: string
    value: number
    unit: string
    created_at: string
}
export interface IDeviceDashboard {
    id: number
    device_uid: string
    name: string
    location: string
    sensors: ISensor[]
}

const API_BASE_URL = 'http://localhost:8000'

export function getApiBaseUrl(): string{
    return API_BASE_URL
}
export async function getDevices(): Promise<IDevice[]> {
    const response = await fetch(`${API_BASE_URL}/api/devices`)
    if (!response.ok) {
        throw new Error('Failed to fetch devices')
    }

    return response.json()
}
export async function getDevice(
    deviceUid: string
): Promise<IDevice | null>{

    const response = await fetch(
        `${API_BASE_URL}/api/devices/${deviceUid}`
    )
    if (response.status === 404){
        return null
    }
    if (!response.ok){
        throw new Error(`Failed to fetch device: ${deviceUid}`)
    }
    
    return response.json()
}

export async function getDeviceDashboard(
    deviceUid: string
): Promise<IDeviceDashboard | null> {
    const response = await fetch(`${API_BASE_URL}/api/devices/${deviceUid}/dashboard`)

    if(!response.ok){
        throw new Error('Failed to fetch device dashboard')
    }
    return response.json()

    
}




