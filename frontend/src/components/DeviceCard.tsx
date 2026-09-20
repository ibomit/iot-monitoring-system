import { Cpu } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import type { IDevice } from '../services/api'

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
            <div className="device-card-header">

                <div className="device-card-icon">
                    <Cpu size={48} />
                </div>
                <div className="device-card-title">
                    <h3>{device.name}</h3>

                </div>
            </div>
            <div className="device-card-info">

                <p>
                    <strong>Device:</strong>{device.device_uid}
                </p>
                <p>
                    <strong>Location:</strong>{device.location}
                </p>
            </div>
            <div className="device-card-footer">
                <span>3 sensors</span>
                <span>Last seen: 2 min ago</span>
            </div>
        </button>

    )
}

export default DeviceCard