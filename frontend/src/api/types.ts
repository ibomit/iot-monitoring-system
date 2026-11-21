export interface IDevice {
  id: number;
  device_uid: string;
  name: string;
  location: string;
  created_at: string;
  last_seen_at: string | null;
  status: DeviceStatus;
}

export type DeviceStatus = "online" | "offline" | "unknown";
export interface ISensor {
  sensor_uid: string;
  name: string;
  sensor_type: string;
  latest_measurements: IMeasurement[];
}
export interface IMeasurement {
  id: number;
  sensor_id: number;
  metric: string;
  value: number;
  unit: string;
  created_at: string;
}
export interface IMeasurementBucket {
  metric: string;
  unit: string;
  bucket_start: string;
  value: number;
  count: number;
}
export interface IDeviceDashboard {
  device_uid: string;
  name: string;
  location: string;
  last_seen_at: string | null;
  status: DeviceStatus;
  sensors: ISensor[];
}
export interface DeviceDeleteResponse {
  success: boolean;
  message: string;
}

export interface IUser {
  id: number;
  username: string;
  email: string;
  role: string;
  created_at: string;
}
export interface ITokenResponse {
  access_token: string;
  token_type: string;
}


