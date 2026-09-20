import type { ISensor } from '../services/api'
// import { useNavigate } from 'react-router-dom'
import {
    Card,
    CardHeader
} from "@/components/ui/card"
import './SensorCard.css'


interface SensorCardProp {
    sensor: ISensor
}

function SensorCard({
    sensor
}: SensorCardProp) {
    // const navigate = useNavigate()
    return (
        <button
            type="button"
            className="sensor-card"
            // onClick={() => navigate(`/devices/${device.device_uid}`)}
        >
            <h3>{sensor.name}</h3>
            <p>
                <strong>Sensor:</strong>{sensor.sensor_uid}
            </p>
            <p>
                <strong>Type:</strong>{sensor.sensor_type}
            </p>
        </button>
    )
}

export default SensorCard