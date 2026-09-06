import type { Device } from "../api/api"
import DeviceCard from "../components/DeviceCard"
import './Devices.css'
interface DevicesTableProps {
    devices: Device[]
}

function Devices() {
    let devices: Device[] = [
        {
            id: 1,
            device_uid: "esp_testDevice",
            name: "testDevice",
            location: "lab",
            created_at: "26.09.2024"

        },
        {
            id: 2,
            device_uid: "esp_testDevice2",
            name: "testDevice2",
            location: "lab",
            created_at: "26.09.2024"
        }
    ]


    return (
        <div>
            <div className="devices-header">
                <div>

                    <h1>
                        Devices
                    </h1>
                    <p>
                        List of all devices
                    </p>
                </div>
                <input
                    type="text"
                    placeholder="Search devices..."
                />
            </div>
            <main className="main">

                <div>
                    <DevicesTable
                        devices={devices} />
                </div>
            </main>

        </div>
    )
}

function DevicesTable({ devices }: DevicesTableProps) {
    return (
        <div className="devices">
            {devices.map((device) => (
                <DeviceCard
                    key={device.id}
                    device={device}
                    onClick={() => { }}
                />
            ))}
        </div>
    )
}

export default Devices