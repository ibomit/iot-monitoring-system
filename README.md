# IoT Monitoring System

[![CI](https://github.com/ibomit/iot-monitoring-system/actions/workflows/ci.yml/badge.svg)](https://github.com/ibomit/iot-monitoring-system/actions/workflows/ci.yml)

An end-to-end IoT monitoring system. ESP32 devices (or a Python simulator) send sensor measurements over HTTP to a FastAPI backend, which stores them in PostgreSQL and serves a React dashboard.

> **Status:** under active development. Devices, sensors and measurements work end to end, and the dashboard lists devices and their sensors. Latest values, charts and the login screen are still to come (see the Roadmap below).

Built as a personal full-stack and IoT portfolio project.

## ✨ Features

- Create devices in the dashboard, then let the ESP32 register its own sensors automatically
- Multiple sensors per device and multiple metrics per sensor (a DHT sensor reports temperature and humidity)
- Batched measurement uploads that are saved all-or-nothing
- Device status (online, offline, unknown) derived from the last measurement received
- Firmware that keeps retrying with backoff when Wi-Fi or the backend is down
- JWT authentication with argon2 password hashing and an admin role
- Alembic migrations, a pytest suite, Docker images and a CI pipeline

## 🏗️ Architecture

```text
 ┌──────────────┐   ┌──────────────┐
 │    ESP32     │   │  Simulator   │
 │ fake or real │   │   (Python)   │
 │   sensors    │   │              │
 └──────┬───────┘   └──────┬───────┘
        └────────┬─────────┘
                 │ HTTP + JSON
                 ▼
         ┌───────────────┐   JSON    ┌─────────────────┐
         │    FastAPI    │◄─────────►│ React dashboard │
         │    backend    │           │  (Vite + TS)    │
         └───────┬───────┘           └─────────────────┘
                 │ SQLAlchemy
                 ▼
         ┌───────────────┐
         │  PostgreSQL   │
         └───────────────┘
```

The backend keeps its layers separate:

- **Routers** handle HTTP
- **Services** hold the business logic and raise domain exceptions (`NotFoundError`, `ConflictError`, `BadRequestError`)
- **Schemas** (Pydantic) define the API contract
- **Models** (SQLAlchemy) map to the database

One handler in `main.py` turns domain exceptions into 404, 409 and 400 responses.

### Data model

```text
Device 1 ────── * Sensor 1 ────── * Measurement
```

| Table | Main fields |
|---|---|
| `devices` | `device_uid` (unique, identifies the physical device), `name`, `location`, `created_at`, `last_seen_at` |
| `sensors` | `sensor_uid` (unique), `name`, `sensor_type`, `device_id`, `created_at` |
| `measurements` | `sensor_id`, `metric`, `value`, `unit`, `created_at` |
| `users` | `username`, `email`, `password_hash`, `role`, `created_at` |

All timestamps are stored as timezone-aware UTC and returned as ISO 8601 strings ending in `Z`.

## 🛠️ Tech Stack

| Area | Technology |
|---|---|
| Backend | Python 3.14, FastAPI, SQLAlchemy 2, Pydantic, Alembic, PostgreSQL 17 (psycopg), uv, pytest |
| Frontend | React 19, TypeScript, Vite, React Router, Tailwind CSS, shadcn/ui (Base UI), Lucide |
| Firmware | C++ (Arduino framework), PlatformIO, ESP32 |
| Infrastructure | Docker, Docker Compose, GitHub Actions |

## 🚀 Quick Start

**Prerequisites:** Docker, [uv](https://docs.astral.sh/uv/) and Node.js 22. PlatformIO is only needed for the firmware.

**1. Start PostgreSQL**

```bash
docker compose up -d
```

Adminer (a database browser) is available at http://localhost:8080 with server `postgres`.

**2. Configure the backend.** Create `backend/.env`:

```bash
DATABASE_URL=postgresql+psycopg://iot_user:iot_password@localhost:5432/iot_db
SECRET_KEY=<a random string of at least 32 characters>
```

Generate a key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**3. Apply the migrations and start the API**

```bash
cd backend
uv run alembic upgrade head
bash run.sh
```

The API runs at http://localhost:8000 and its interactive docs at http://localhost:8000/docs.

**4. Start the dashboard** (in a second terminal)

```bash
cd frontend
npm install
npm run dev
```

The dashboard runs at http://localhost:5173.

**5. Send some data.** In the dashboard, click **Add device** and create a device with the UID `simulator-001`. Then, from the repository root:

```bash
uv run --project backend python simulator/sensor_simulator.py
```

The simulator registers two sensors and sends a batch of measurements every 5 seconds. Within about 10 seconds the device shows as **online** (the device list refreshes every 10 seconds).

### Run everything in Docker (optional)

The backend and frontend also have Docker images. They are opt-in, so a plain `docker compose up -d` still starts only PostgreSQL and Adminer.

```bash
docker compose --profile app up -d --build
docker compose --profile app run --rm backend alembic upgrade head
```

The dashboard is then at http://localhost:8081 and the API at http://localhost:8000. Stop a locally running backend first, and make sure `backend/.env` contains a `SECRET_KEY`.

## ⚙️ Configuration

| Where | Variable | Required | Default | Purpose |
|---|---|---|---|---|
| `backend/.env` | `DATABASE_URL` | yes | | PostgreSQL connection string |
| `backend/.env` | `SECRET_KEY` | yes | | JWT signing key (at least 32 characters; the app refuses to start without it) |
| `backend/.env` | `CORS_ORIGINS` | no | `http://localhost:5173` | Comma-separated list of allowed dashboard origins |
| `backend/.env` | `ACCESS_TOKEN_EXPIRE_MINUTES` | no | `60` | JWT lifetime |
| `backend/.env` | `ALGORITHM` | no | `HS256` | JWT algorithm |
| `frontend/.env` | `VITE_API_URL` | no | `http://localhost:8000` | API address used by the browser (copy `frontend/.env.example`; baked in at build time in Docker) |
| `firmware/include/secrets.h` | Wi-Fi and server address | yes | | See the firmware section |

`.env` files and `secrets.h` are gitignored and must never be committed.

## 📚 API

Interactive documentation is generated by FastAPI at http://localhost:8000/docs.

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/devices` | Create a device (`409` if the `device_uid` already exists) |
| `GET` | `/api/devices` | List devices with their status |
| `GET` | `/api/devices/{device_uid}` | Get one device |
| `DELETE` | `/api/devices/{device_uid}` | Delete a device together with its sensors and measurements |
| `GET` | `/api/devices/{device_uid}/dashboard` | Device with its sensors and the latest value of each metric |
| `GET` | `/api/devices/{device_uid}/sensors` | Sensors of a device |
| `GET` | `/api/devices/{device_uid}/measurements/latest` | Latest value per sensor and metric |
| `POST` | `/api/sensors/register` | Register a sensor (idempotent, used by the firmware) |
| `GET` | `/api/sensors` | List sensors |
| `GET` | `/api/sensors/{sensor_uid}/measurements` | History, newest first (`limit` 1 to 1000, optional `start` and `end`) |
| `GET` | `/api/sensors/{sensor_uid}/measurements/latest` | Latest value per metric |
| `POST` | `/api/measurements` | Submit a batch of measurements (used by the firmware) |
| `GET` | `/api/measurements` | Most recent measurements (`limit` 1 to 1000) |
| `POST` | `/api/auth/register` | Create a user |
| `POST` | `/api/auth/login` | Log in and receive a JWT |
| `GET` | `/api/auth/me` | Current user |

### Device contract

This is the contract the ESP32 firmware and the simulator rely on.

Register a sensor. Repeating the request is safe and returns "Sensor already registered":

```http
POST /api/sensors/register
{
  "device_uid": "esp32-001",
  "sensor_uid": "fake-dht-001",
  "name": "DHT Sensor",
  "sensor_type": "DHT"
}
```

Submit measurements. A batch can mix several sensors and is saved all-or-nothing:

```http
POST /api/measurements
{
  "device_uid": "esp32-001",
  "measurements": [
    { "sensor_uid": "fake-dht-001", "metric": "temperature", "value": 22.4, "unit": "celsius" },
    { "sensor_uid": "fake-dht-001", "metric": "humidity", "value": 48.1, "unit": "percent" }
  ]
}
```

Errors devices may see:

| Status | Meaning |
|---|---|
| `404` | `Device not found`, or `Sensor not found: <sensor_uid>` |
| `400` | The sensor belongs to a different device |
| `422` | Invalid input: text fields are limited to 100 characters (`unit`: 50) and a batch to 100 measurements |

A device is **online** if a measurement arrived in the last 2 minutes, **offline** if its last one is older, and **unknown** if it has never reported.

## 🔐 Authentication and Security

Implemented: user registration, login, JWT access tokens, the current-user endpoint, an admin role and argon2 password hashing.

**Current limitation:** during development, the dashboard and device-management endpoints are not protected. The `CurrentUser` and `AdminUser` guards exist but are switched off until the login screen is built, and the device endpoints are public by design. Do not expose the backend to untrusted networks yet. Per-device authentication is on the roadmap.

Other safeguards: secrets live in gitignored files, the app refuses to start without a `SECRET_KEY`, and PostgreSQL and Adminer only listen on `localhost`.

## 📟 ESP32 Firmware

The firmware lives in `firmware/` and is built with PlatformIO. It currently uses fake sensors, so no hardware beyond the board is needed.

**Setup**

1. Copy `firmware/include/secrets.h.example` to `firmware/include/secrets.h` and fill in your Wi-Fi name, password and the backend address, for example `http://192.168.1.20:8000` (the computer running the backend, reachable from the ESP32's network).
2. Create a device in the dashboard whose UID matches `DEVICE_UID` in `firmware/src/main.cpp` (default `esp32-001`).
3. Upload and watch the serial output:

```bash
cd firmware
pio run -t upload
pio device monitor
```

The upload port is set to `/dev/ttyUSB0` in `platformio.ini`; change it for your machine. The PlatformIO IDE extension works as well.

**How it behaves**

```text
Boot ─► connect to Wi-Fi ─► register each sensor ─► every 3 seconds:
                                                     read sensors ─► POST /api/measurements
```

- If a request fails, the batch is kept and retried with exponential backoff (up to 60 seconds), and the sensors are registered again
- If Wi-Fi drops, the firmware reconnects automatically

**Sensors.** All sensors implement a common `Sensor` interface, so the main program does not care whether a sensor is fake or real. Adding a real sensor means implementing `read()` and creating it in `main.cpp`.

```text
Sensor
├── FakeDHTSensor        temperature (celsius), humidity (percent)
├── FakeDistanceSensor   distance (cm)
└── real sensors (planned): DHT22, HC-SR04, PIR motion
```

## 🧪 Development

**Tests.** Start PostgreSQL, then:

```bash
cd backend
uv run pytest
```

The tests run against a separate `<database name>_test` database (for example `iot_db_test`), which is created automatically. They never touch the development database. To use a different one, set `TEST_DATABASE_URL`; its name must end with `_test`.

**Migrations.** From `backend/`:

```bash
uv run alembic revision --autogenerate -m "Describe the change"
uv run alembic upgrade head
uv run alembic current
```

A model change needs a migration; CI fails if the models and migrations disagree.

**Frontend checks.** From `frontend/`: `npm run lint` and `npm run build`.

**Continuous integration.** `.github/workflows/ci.yml` runs on every pull request. It applies the migrations and checks that they match the models, runs the backend tests, lints and builds the frontend, and builds both Docker images.

### Project structure

```text
iot-monitoring-system/
├── backend/
│   ├── app/
│   │   ├── routers/          # HTTP layer: auth, devices, sensors, measurements
│   │   ├── services/         # business logic
│   │   ├── schemas/          # Pydantic request and response models (the API contract)
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── exceptions.py     # domain exceptions, mapped to HTTP errors in main.py
│   │   ├── auth.py           # current-user and admin dependencies
│   │   ├── security.py       # password hashing and JWT
│   │   ├── dependencies.py   # shared database-session dependency
│   │   ├── database.py       # engine and session
│   │   └── main.py           # FastAPI app, CORS, error handler
│   ├── alembic/              # database migrations
│   ├── tests/                # pytest suite: devices, device flow, auth
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── pages/            # Devices, DeviceDashboard
│   │   ├── components/       # DeviceCard, SensorCard, sidebar, theme toggle
│   │   │   └── ui/           # shadcn/ui primitives
│   │   └── services/api.ts   # all backend calls and API types
│   ├── Dockerfile
│   └── nginx.conf
├── firmware/                 # ESP32 (PlatformIO)
│   ├── include/secrets.h.example
│   ├── src/                  # main.cpp, network/ApiClient, sensors/
│   └── platformio.ini
├── simulator/sensor_simulator.py
├── .github/workflows/ci.yml
├── docker-compose.yml
└── README.md
```

## 🗺️ Roadmap

**Done**

- [x] Backend API for devices, sensors, measurements and authentication
- [x] PostgreSQL with Alembic migrations
- [x] ESP32 firmware with fake sensors, automatic sensor registration and retry with backoff
- [x] Python sensor simulator
- [x] Dashboard: searchable device list with status, add device, device page with its sensors, dark mode
- [x] Backend tests, Docker images and CI

**Next**

- [ ] Show the latest measurements on the device page
- [ ] Charts for historical data (the API already supports time ranges)
- [ ] Delete devices from the dashboard (the API endpoint exists)
- [ ] Login page, then enable the authentication guards and admin-only device management
- [ ] Device authentication and secure device provisioning
- [ ] Real sensors (DHT22, HC-SR04, PIR)

**Later**

- [ ] Pagination for the device and sensor lists
- [ ] A health check that also verifies the database

## 👨‍💻 Author

Built as a personal full-stack and IoT portfolio project.
