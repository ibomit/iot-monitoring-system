import type { Device } from '../services/api'
import './DeviceCard.css'


interface DeviceCardProps {
    device: Device
    onClick: () => void
}
// TODO: Add OnClick handler

function DeviceCard({
    device,
    onClick
}: DeviceCardProps) {
    return (
        <button
            type="button"
            className="device-card"
            onClick={onClick}
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