import type { IDevice } from '../services/api'
import { useNavigate } from 'react-router-dom'
import { 
    Card,
    CardHeader
 } from "@/components/ui/card"
import './DeviceCard.css'


interface DeviceCardProps {
    device: IDevice
}

function DeviceCard({
    device
}: DeviceCardProps) {
    const navigate = useNavigate()
    return (
            <button
                type="button"
                className="device-card"
                onClick={() => navigate(`/devices/${device.device_uid}`)}
                >
                <h3>{device.name}</h3>
                <p>
                    <strong>Device:</strong>{device.name}
                </p>
                <p>
                    <strong>Location:</strong>{device.location}
                </p>
            </button>

    )
}

export default DeviceCard