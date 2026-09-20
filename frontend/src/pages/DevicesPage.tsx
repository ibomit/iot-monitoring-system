import { useState, useEffect } from 'react'
import { createDevice, deleteDevice, getDevices, type DeviceDeleteResponse, type IDevice } from "../services/api"
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { toast } from "@/components/ui/toast"

import { Field, FieldGroup } from "@/components/ui/field"

import DeviceCard from "../components/DeviceCard"
import './DevicesPage.css'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
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

    async function handleAddDeviceSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        console.log("Form submitted")
        const formData = new FormData(event.currentTarget)

        const device_name = formData.get('device_name') as string
        const device_uid = formData.get('device_uid') as string
        const device_location = formData.get('device_location') as string

        console.log('Adding device:', { device_name, device_uid, device_location })

        try {
            const response = await createDevice(
                device_name,
                device_uid,
                device_location
            )
            console.log('Response:', { response })
            toast.add({
                title: "Device Added",
                description: `Device ${device_name} has been added successfully.`,
                type: "success",
            })
            
        } catch (err) {
        console.error('Failed to create device:', err)
        
        if (
            err instanceof Error &&
            'status' in err &&
            err.status === 409  
        ){
            toast.add({
                title: "Error",
                description: `Device with UID ${device_uid} already exists.`,
                type: "error",
            })
            return
        }
        toast.add({
            title: "Error",
            description: `Failed to add device ${device_name}. Please try again.`,
            type: "error",
        })
    }
    await loadDevices()
}

async function handleDeleteDevice(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    const deviceUid = formData.get('device_uid') as string
    console.log('Deleting device:', { deviceUid })
    const response: Promise<DeviceDeleteResponse> = deleteDevice(deviceUid)
    console.log('Response:', { response })
}

return (
    <div>
        <div className="devices-header">
            <div>

                <h1>
                    Devices
                </h1>
                <p>
                    List of all registered devices
                </p>
            </div>
        </div>
        <div className="flex flex-wrap items-center gap-2 md:flex-row">
            {/* <Button onClick={() => { window.location.href = '/register-device' }}> */}
            {/* <ButtonGroup> */}
            <Dialog>
                <DialogTrigger render={<Button>Add Device</Button>} />
                <DialogContent className="sm:max-w-sm">
                    <form onSubmit={handleAddDeviceSubmit}>
                        <DialogHeader>
                            <DialogTitle>Add Device</DialogTitle>
                            <DialogDescription>
                                Add a new device to the system. Please fill in the required information and click "Add Device" to proceed.
                            </DialogDescription>
                        </DialogHeader>

                        <FieldGroup>
                            <Field>
                                <Label htmlFor="device_name">Name</Label>
                                <Input id="device_name" name="device_name" required />
                            </Field>
                            <Field>
                                <Label htmlFor="device_uid">Device UID</Label>
                                <Input id="device_uid" name="device_uid" required />
                            </Field>
                            <Field>
                                <Label htmlFor="device_location">Location</Label>
                                <Input id="device_location" name="device_location" required />
                            </Field>
                        </FieldGroup>
                        <DialogFooter>
                            <DialogClose render={<Button variant="outline">Cancel</Button>} />
                            <DialogClose render={<Button type="submit">Add Device</Button>} />
                        </DialogFooter>
                    </form >
                </DialogContent>
            </Dialog>
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