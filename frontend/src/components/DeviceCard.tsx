import type { Device } from '../api/api'
import './DeviceCard.css'


interface DeviceCardProps {
    device: Device
    onClick: () => void
}

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