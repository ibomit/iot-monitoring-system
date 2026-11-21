import { toApiError } from "./helpers";
import type {
  DeviceDeleteResponse,
  IDevice,
  IDeviceDashboard,
  IMeasurement,
  IMeasurementBucket,
  ITokenResponse,
  IUser,
} from "./types";

let accessToken: string | null = null;
let refreshPromise: Promise<boolean> | null = null;

const API_BASE_URL: string = (
  import.meta.env.VITE_API_URL ?? "http://localhost:8000"
).replace(/\/$/, "");

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      cache: "no-store",
    });
    return response.ok;
  } catch {
    return false;
  }
}

export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const send = () => {
    const headers = new Headers(init.headers);
    if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
    return fetch(`${API_BASE_URL}${path}`, { ...init, headers, credentials: "include" });
  }
  const response = await send()
  if (response.status !== 401) return response

  // The access token has expired (or is missing). Refresh it, but only once:
  // if a refresh is already running, wait for that one instead of starting another.
  refreshPromise ??= refreshSession().finally(() => {
    refreshPromise = null;
  });
  const refreshed = await refreshPromise;

  // Not logged in any more: hand the 401 back to the caller.
  if (!refreshed) return response;

  // Try once more. send() reads the new accessToken.
  return send();
}

export async function getDevices(): Promise<IDevice[]> {
  const response = await apiFetch("/api/devices");
  if (!response.ok) {
    throw new Error("Failed to fetch devices");
  }

  return response.json();
}

export async function refreshSession(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });
    if (!response.ok) {
      accessToken = null;
      return false;
    }

    const data: ITokenResponse = await response.json();
    accessToken = data.access_token;
    return true;
  } catch {
    accessToken = null;
    return false;
  }
}

export async function logout(): Promise<void> {
  try {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
  } catch {
    // Server unreachable: still log out locally.
  } finally {
    accessToken = null;
  }
}

export async function getCurrentUser(): Promise<IUser> {
  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    method: "GET",
    headers: { Authorization: `Bearer ${accessToken}` },
    credentials: "include",
  });
  if (!response.ok) throw await toApiError(response, "Failed to load user");
  return response.json();
}

export async function login(username: string, password: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    body: new URLSearchParams({ username, password }),
    credentials: "include",
  });
  if (!response.ok) {
    accessToken = null;
    throw await toApiError(response, "Failed to log in");
  }
  const data: ITokenResponse = await response.json();
  accessToken = data.access_token;
}

export async function createDevice(
  device_name: string,
  device_uid: string,
  device_location: string,
): Promise<IDevice> {
  const response = await apiFetch('/api/devices', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: device_name,
      device_uid: device_uid,
      location: device_location,
    }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    const error = new Error(
      errorData.detail ?? "Failed to create device",
    ) as Error & {
      status: number;
    };
    error.status = response.status;
    throw error;
  }
  return response.json();
}

export async function deleteDevice(
  deviceUid: string,
): Promise<DeviceDeleteResponse> {
  const response = await apiFetch(`/api/devices/${deviceUid}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error(`Failed to delete device: ${deviceUid}`);
  }

  return response.json();
}

export async function getDevice(deviceUid: string): Promise<IDevice | null> {
  const response = await apiFetch(`/api/devices/${deviceUid}`);
  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new Error(`Failed to fetch device: ${deviceUid}`);
  }

  return response.json();
}

export async function getDeviceDashboard(
  deviceUid: string,
): Promise<IDeviceDashboard | null> {
  const response = await apiFetch(`/api/devices/${deviceUid}/dashboard`,
  );

  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new Error("Failed to fetch device dashboard");
  }
  return response.json();
}

export async function getLatestSensorMeasurements(
  sensorUid: string,
): Promise<IMeasurement[]> {
  const response = await apiFetch(`/api/sensors/${encodeURIComponent(sensorUid)}/measurements/latest`,
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      typeof errorData?.detail === "string"
        ? errorData.detail
        : "Failed to fetch latest sensor measurements",
    );
  }

  return response.json();
}

export async function getSensorMeasurements(
  sensorUid: string,
  limit: number = 100,
  start: string | null = null,
  end: string | null = null,
): Promise<IMeasurement[]> {
  // The API returns the newest measurements first.
  // start/end must be ISO 8601 strings, ideally date.toISOString() (UTC, ends in Z).
  const params = new URLSearchParams({ limit: String(limit) });
  if (start) {
    params.set("start", start);
  }
  if (end) {
    params.set("end", end);
  }

  const response = await apiFetch(`/api/sensors/${encodeURIComponent(sensorUid)}/measurements?${params}`,
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      typeof errorData?.detail === "string"
        ? errorData.detail
        : "Failed to fetch sensor measurements",
    );
  }

  return response.json();
}

export async function getSensorMeasurementBuckets(
  sensorUid: string,
  start: string,
  end: string | null = null,
  maxPoints: number = 300,
): Promise<IMeasurementBucket[]> {
  // Averages per metric over time buckets, oldest first.
  // start/end must be ISO 8601 strings, ideally date.toISOString() (UTC, ends in Z).
  const params = new URLSearchParams({
    start,
    max_points: String(maxPoints),
  });
  if (end) {
    params.set("end", end);
  }

  const response = await apiFetch(`/api/sensors/${encodeURIComponent(sensorUid)}/measurements/buckets?${params}`,
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(
      typeof errorData?.detail === "string"
        ? errorData.detail
        : "Failed to fetch sensor measurement buckets",
    );
  }

  return response.json();
}
