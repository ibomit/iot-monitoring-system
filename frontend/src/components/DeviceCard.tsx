import { CalendarDays, ChevronRight, Cpu, MapPin } from 'lucide-react'
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
    const registeredDate = new Intl.DateTimeFormat(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    }).format(new Date(device.created_at))

    return (
        <button
            type="button"
            className="device-card"
            aria-label={`Open ${device.name} device dashboard`}
            onClick={() => navigate(`/devices/${device.device_uid}`)}
        >
            <div className="device-card-topline">
                <span className={`device-status status-${device.status}`}>
                    <span /> {device.status}
                </span>
                <ChevronRight className="device-card-arrow" aria-hidden="true" />
            </div>
            <div className="device-card-header">
                <div className="device-card-icon">
                    <Cpu aria-hidden="true" />
                </div>
                <div className="device-card-title">
                    <h3>{device.name}</h3>
                    <span>{device.device_uid}</span>
                </div>
            </div>
            <div className="device-card-info">
                <p><MapPin aria-hidden="true" />{device.location}</p>
                <p><CalendarDays aria-hidden="true" />Registered {registeredDate}</p>
            </div>
            <div className="device-card-footer">
                <span>View device dashboard</span>
                <span className="device-card-action">Open <ChevronRight aria-hidden="true" /></span>
            </div>
        </button>

    )
}

export default DeviceCard