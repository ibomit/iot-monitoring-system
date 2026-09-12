export interface Device {
    id: number
    device_uid: string
    name: string
    location: string
    created_at: string
}

export interface DeviceDashboard {
    id: number
    device_uid: string
    name: string
    location: string
    // sensors: ...
}

const API_BASE_URL = 'http://localhost:8000'

export function getApiBaseUrl(): string{
    return API_BASE_URL
}
export async function getDevices(): Promise<Device[]> {
    const response = await fetch(`${API_BASE_URL}/api/devices`)
    if (!response.ok) {
        throw new Error('Failed to fetch devices')
    }

    return response.json()
}
export async function getDevice(
    deviceUid: string
): Promise<Device | null>{

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
) {
    const response = await fetch(`${API_BASE_URL}/api/devices/${deviceUid}/dashboard`)

    if(!response.ok){
        throw new Error('Failed to fetch device dashboard')
    }
    return response.json()

    
}




