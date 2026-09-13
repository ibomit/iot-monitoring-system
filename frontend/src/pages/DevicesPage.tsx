import { useState, useEffect } from 'react'
import { getDevices, type IDevice } from "../services/api"

import DeviceCard from "../components/DeviceCard"
import './DevicesPage.css'
interface DevicesTableProps {
    devices: IDevice[],
    error: string | null,
    loading: boolean
}

function Devices() {

    const [devices, setDevices] = useState<IDevice[]>([]);
    const [searchQuery, setSearchQuery] = useState<string>('')
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true)

    const filteredDevices = devices.filter((device) =>
        device.name
            .toLowerCase()
            .includes(searchQuery.toLowerCase())
    )

    useEffect(() => {
        loadDevices()
    }, [])

    async function loadDevices() {
        setLoading(true)
        try {
            const data = await getDevices()
            setDevices(data)
            setError(null)
        } catch (err) {
            setError('Failed to load devices...')
            console.log(err)
        } finally {
            setLoading(false)
        }
    }


    return (
        <div>
            <div className="devices-header">
                <div>

                    <h1>
                        Devices
                    </h1>
                    <p>
                        List of all deviceDeviceDashboards
                    </p>
                </div>
            </div>
            <div className=''>
                <input
                    type="text"
                    placeholder="Search for a device..."
                    className="search-input"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>
            <main className="main">
                <div>
                    <DevicesTable
                        devices={filteredDevices}
                        error={error}
                        loading={loading} />
                    {/* <DevicesTable

devices={devices2} /> */}
                </div>
            </main>


        </div>
    )
}

function DevicesTable({ devices, error, loading }: DevicesTableProps) {
    return (
        <>
            {error && <div className="error-message">{error}</div>}
            {loading ? (
                <div className="loading">Loading...</div>
            ) : (
                <div className="devices-grid">
                    {devices.map((device) => (
                        <DeviceCard
                            key={device.id}
                            device={device}
                            // onClick={() => { }}
                        />
                    ))}
                </div>
            )}
        </>
    )
}

export default Devices