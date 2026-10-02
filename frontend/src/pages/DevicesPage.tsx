import { useState, useEffect } from 'react'
import { MapPin, Plus, RefreshCw, Search, Server, Wifi } from 'lucide-react'
import { createDevice, getDevices, type IDevice } from "../services/api"
import { Button } from "@/components/ui/button"
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
    loading: boolean,
    hasSearchQuery: boolean,
    onRetry: () => void
}

const DEVICES_REFRESH_INTERVAL_MS = 10000

function Devices() {

    const [devices, setDevices] = useState<IDevice[]>([]);
    const [searchQuery, setSearchQuery] = useState<string>('')
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true)
    const [dialogOpen, setDialogOpen] = useState(false)
    const [submitting, setSubmitting] = useState(false)

    const filteredDevices = devices.filter((device) =>
        device.name
            .toLowerCase()
            .includes(searchQuery.toLowerCase())
    )

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

    useEffect(() => {
        let cancelled = false

        // Silent refresh: does not toggle the loading state, so the grid doesn't flash
        async function refreshDevices() {
            try {
                const data = await getDevices()
                if (!cancelled) {
                    setDevices(data)
                    setError(null)
                }
            } catch (err) {
                if (!cancelled) {
                    setError('Failed to load devices...')
                    console.log(err)
                }
            } finally {
                if (!cancelled) {
                    setLoading(false)
                }
            }
        }

        void refreshDevices()
        const intervalId = window.setInterval(
            refreshDevices,
            DEVICES_REFRESH_INTERVAL_MS
        )

        return () => {
            cancelled = true
            window.clearInterval(intervalId)
        }
    }, [])

    async function handleAddDeviceSubmit(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault()
        console.log("Form submitted")
        const formData = new FormData(event.currentTarget)

        const device_name = formData.get('device_name') as string
        const device_uid = formData.get('device_uid') as string
        const device_location = formData.get('device_location') as string

        console.log('Adding device:', { device_name, device_uid, device_location })

        setSubmitting(true)
        try {
            await createDevice(
                device_name,
                device_uid,
                device_location
            )
        } catch (err) {
            console.error('Failed to create device:', err)

            // Keep the dialog open so the user can fix the input
            if (
                err instanceof Error &&
                'status' in err &&
                err.status === 409
            ) {
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
            return
        } finally {
            setSubmitting(false)
        }

        toast.add({
            title: "Device Added",
            description: `Device ${device_name} has been added successfully.`,
            type: "success",
        })
        setDialogOpen(false)
        await loadDevices()
    }

// async function handleDeleteDevice(event: React.SubmitEvent<HTMLFormElement>) {
//     event.preventDefault()
//     const formData = new FormData(event.currentTarget)
//     const deviceUid = formData.get('device_uid') as string
//     console.log('Deleting device:', { deviceUid })
//     const response: Promise<DeviceDeleteResponse> = deleteDevice(deviceUid)
//     console.log('Response:', { response })
// }

return (
    <div className="devices-page">
        <section className="devices-hero">
            <div>
                <p className="eyebrow">Fleet overview</p>
                <h1>Devices</h1>
                <p className="devices-description">Monitor and manage every registered device from one place.</p>
            </div>
            <div className="devices-hero-mark" aria-hidden="true">
                <Wifi />
            </div>
        </section>

        <section className="device-stats" aria-label="Device summary">
            <div className="stat-card">
                <span className="stat-icon stat-icon-blue"><Server /></span>
                <div><span className="stat-label">Total devices</span><strong>{devices.length}</strong></div>
            </div>
            <div className="stat-card">
                <span className="stat-icon stat-icon-green"><Wifi /></span>
                <div><span className="stat-label">Online devices</span><strong>{devices.filter((device) => device.status === 'online').length}</strong></div>
            </div>
            <div className="stat-card">
                <span className="stat-icon stat-icon-amber"><MapPin /></span>
                <div><span className="stat-label">Locations</span><strong>{new Set(devices.map((device) => device.location)).size}</strong></div>
            </div>
        </section>

        <section className="devices-toolbar" aria-label="Device controls">
            <div className="device-search">
                <Search className="device-search-icon" aria-hidden="true" />
                <input
                    type="search"
                    placeholder="Search devices..."
                    aria-label="Search devices"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>
            <div className="device-actions">
                <Button variant="outline" size="icon" onClick={() => void loadDevices()} disabled={loading} aria-label="Refresh devices" title="Refresh devices">
                    <RefreshCw className={loading ? 'animate-spin' : ''} />
                </Button>
            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                    <DialogTrigger render={<Button><Plus /> Add device</Button>} />
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
                                <Input id="device_name" name="device_name" maxLength={100} required />
                            </Field>
                            <Field>
                                <Label htmlFor="device_uid">Device UID</Label>
                                <Input id="device_uid" name="device_uid" maxLength={100} required />
                            </Field>
                            <Field>
                                <Label htmlFor="device_location">Location</Label>
                                <Input id="device_location" name="device_location" maxLength={100} required />
                            </Field>
                        </FieldGroup>
                        <DialogFooter>
                            <DialogClose render={<Button variant="outline">Cancel</Button>} />
                            <Button type="submit" disabled={submitting}>Add Device</Button>
                        </DialogFooter>
                    </form >
                </DialogContent>
            </Dialog>
            </div>
        </section>

        <section className="devices-section" aria-labelledby="device-list-heading">
            <div className="section-heading">
                <div>
                    <h2 id="device-list-heading">Your devices</h2>
                    <p>{filteredDevices.length} of {devices.length} devices shown</p>
                </div>
            </div>
                <DevicesTable
                    devices={filteredDevices}
                    error={error}
                    loading={loading}
                    hasSearchQuery={searchQuery.trim().length > 0}
                    onRetry={() => void loadDevices()} />
        </section>
    </div>
)
}

function DevicesTable({ devices, error, loading, hasSearchQuery, onRetry }: DevicesTableProps) {
    return (
        <>
            {error && (
                <div className="device-state error-message" role="alert">
                    <p>{error}</p>
                    <Button variant="outline" size="sm" onClick={onRetry}>Try again</Button>
                </div>
            )}
            {loading ? (
                <div className="device-state loading" aria-live="polite">
                    <RefreshCw className="animate-spin" />
                    <p>Loading your devices...</p>
                </div>
            ) : devices.length === 0 && !hasSearchQuery && !error ? (
                <div className="device-state empty-state">
                    <Server />
                    <h3>No devices yet</h3>
                    <p>Add your first device to start monitoring your fleet.</p>
                </div>
            ) : devices.length === 0 && hasSearchQuery ? (
                <div className="device-state empty-state">
                    <Search />
                    <h3>No matches found</h3>
                    <p>Try a different device name or clear your search.</p>
                </div>
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