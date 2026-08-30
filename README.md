# IoT Monitoring System 

An IoT monitoring system designed to collect sensor data from ESP32 devices and display it through a web-based dashboard.

The Project is currently under development and is being built step by step as a full-stack IoT application.

## 🎯 Project Goals

The main goal of this project is to build a complete IoT monitoring system that can:

- Collect data from multiple sensors connected to ESP32 devices
- Send sensor measurements to a backend API
- Automatically register sensors connected to a device
- Store devices, sensors, and measurements in PostgreSQL
- Monitor multiple ESP32 devices
- Support multiple sensors per device
- Display sensor data in a web dashboard
- Visualize sensor activity and movement
- Provide an extensible architecture for future sensor implementations

## 🏗️ Project Architecture

The planned architecture is: 
```
                ┌─────────────────────┐
                │       ESP32         │
                │                     │
                │  ┌───────────────┐  │
                │  │   Sensor      │  │
                │  │  Interface    │  │
                │  └───────┬───────┘  │
                │          │          │
                │   ┌──────┴──────┐   │
                │   │             │   │
                │ Fake Sensors  Real  │
                │              Sensors│
                │   │             │   │
                └───┼─────────────┼───┘
                    │
                    │ HTTP + JSON
                    ▼
             ┌───────────────┐
             │   FastAPI     │
             │    Backend    │
             └───────┬───────┘
                     │
                     │ SQLAlchemy
                     ▼
             ┌───────────────┐
             │ PostgreSQL    │
             │   Database    │
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │ React Frontend│
             │   Dashboard   │
             └───────────────┘
 ```

## 📁 Project Structure

```iot-monitoring-system/
│
iot-monitoring-system/
│
├── backend/                   # FastAPI backend application
│   │
│   ├── app/
│   │   ├── routers/           # API routers
│   │   │   ├── devices.py
│   │   │   ├── sensors.py
│   │   │   └── measurements.py
│   │   │
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   │   ├── device.py
│   │   │   ├── sensor.py
│   │   │   └── measurement.py
│   │   │
│   │   ├── database.py        # Database configuration
│   │   ├── models.py          # SQLAlchemy models
│   │   └── main.py            # FastAPI application
│   │
│   ├── alembic/               # Database migrations
│   └── pyproject.toml
│
├── firmware/                  # ESP32 firmware
│   ├── include/
│   └── src/
│       ├── sensors/
│       ├── network/
│       └── main.cpp
│
├── frontend/                  # React dashboard
│
├── simulator/                 # Sensor simulator
│
├── docs/                      # Project documentation
│
├── docker-compose.yml
│
├── README.md
│
└── .gitignore
```
## 🛠️ Tech Stack

### Backend
- Python 
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- psycopg 
- uv
### Firmware
- C++
- ESP32
- Arduino Framework
- PlatformIO
### Database
- PostgreSQL
- Docker

### Planned
- React
- JavaScript
- Data visualization libraries

## ⚙️ Backend Setup

```bash
cd backend
```
Run the FastAPI development server:
```bash
uv run fastapi dev app/main.py 
```
or 
```bash
bash run.sh
```
The API will be available at: 
http://127.0.0.1:8000

## 📚 API Documentation
FastAPI automatically generates interactive API documentation.
Once the backend is running, open:
```
http://127.0.0.1:8000/docs
```
The API is organized into the following Swagger groups:
- Health
- Devices
- Sensors
- Measurements

The `/docs` page contains the complete and up-to-date API reference, including: 
- Available endpoints
- Request schemas
- Response schemas
- Validation rules
- Interactive API testing


## 🤖 Sensor Simulator

The project includes a Python-based sensor simulator for testing the backend without physical ESP32 hardware.

The simulator:

- Simulates an IoT device
- Registers sensors with the backend
- Generates random sensor measurements
- Sends measurements to the FastAPI API

This allows the backend to be tested using the same Device → Sensor → Measurement architecture as the ESP32 firmware.

### Running the Simulator

Make sure the FastAPI backend is running first:

```bash
cd backend
uv run fastapi dev app/main.py
```
Then, in a separate terminal:
```bash
uv run python simulator/sensor_simulator.py
```
## 🗄️ Database
The project uses PostgreSQL to store: 
- Devices
- Sensors
- Measurements

PostgreSQL runs inside a Docker container 
### Database Relationships
```
Device 1 ────── * Sensor 1 ────── * Measurement
```
A device can have multiple Sensors.

A sensor can have multiple measurements

### Database Structure
```
┌───────────────┐
│    Devices    │
├───────────────┤
│ id            │
│ device_uid    │
│ name          │
│ location      │
│ created_at    │
└───────┬───────┘
        │
        │ One Device
        │
        │ has many
        ▼
┌───────────────┐
│    Sensors    │
├───────────────┤
│ id            │
│ sensor_uid    │
│ name          │
│ sensor_type   │
│ device_id     │
│ created_at    │
└───────┬───────┘
        │
        │ One Sensor
        │
        │ has many
        ▼
┌────────────────┐
│  Measurements  │
├────────────────┤
│ id             │
│ sensor_id      │
│ metric         │
│ value          │
│ unit           │
│ created_at     │
└────────────────┘
```
### 🐘 Running PostgreSQL
Start the database:

```bash
 docker compose up -d
```

Stop the database:

```bash
docker compose down
```

### 🔄 Database Migrations
Database schema changes are managed using Alembic.

Create a migration:

```bash
uv run alembic revision --autogenerate -m "Migration description" 
```

Apply migrations: 

```bash
uv run alembic upgrade head
```

Check the current migration version: 

```bash
uv run alembic current
```

## ⚙️ Environment Variables
The database connection is configured using environment variables. 

Example ```.env``` file: 

```py
DATABASE_URL=postgresql+psycopg://<user>:<password>@localhost:5432/<db>
```

The ```.env``` file should not be commited to Git

## ⚙️ ESP32 Firmware
The project includes firmware for an ESP32 microcontroller, located in the `firmware/` directory.

The ESP32 firmware is developed using:
- PlatformIO
- Arduino framework
- Espressif ESP32 platform
- C++

### 📶 Wi-Fi Connection
The ESP32 connects to a local Wi-Fi network before communicating with the backend. 
Wi-Fi credentials are stored separately from the main firmware code.

Example:
```cpp
#define WIFI_SSID "your-wifi"
#define WIFI_PASSWORD "your-password"
```
Sensitive Credentials should not be commited to Git. During development, the sensitive Credentials are stored under ```iot-monitoring-system/firmware/include/secrets.h```. 

### 🌐 ESP32 to Backend Communication
The ESP32 communicates with the backend using: 

```
 HTTP + JSON
```
 The firmware uses a reusable ```ApiClient``` responsible for communication with the backend.

 The API client handles:
 - Sensor registration
 - Measurement submission
 - HTTP request
 - JSON payload construction
 - HTTP response handling

### 🤖 Firmware Architecture
The ESP32 firmware uses an abstract ```Sensor``` interface.

This allows different sensor implementations to share the same interface.

```
Sensor
│
├── FakeDHTSensor
│
├── FakeDistanceSensor
│
└── Future Real Sensors
    │
    ├── DHT22
    ├── HC-SR04
    ├── PIR Motion Sensor
    └── Other Sensors
```
The main application communicates with sensors through the common ```Sensor``` interface. This means the application does not need to know whether a sensor is Fake or Real. This architecture makes it easier to add new sensor implementations without significantly changing the rest of the application.

### Fake Sensors
Fake sensors are currently used for development and testing. 

The project currently includes:
- Fake DHT Sensor 
- Fake Distance Sensor

### Fake DHT Sensor
Generates random: 
- Temperature
- Humidity 

Example: 
```
temperature: 22.4 celsius
humidity: 48.1 percent
```
### Fake Distance Sensor

Generates random distance measurements.

Example:
```
distance: 410.7 cm
```
Fake sensors allow the complete system to be tested without requiring physical hardware.

Future real sensor implementations can use the same architecture.

### 🔄 Sensor Registration Flow
When the ESP32 starts, its sensors can register themselves with the backend. 
```
ESP32 starts
      │
      ▼
Connect to Wi-Fi
      │
      ▼
Register Sensors
      │
      ▼
Backend checks Device
      │
      ▼
Sensor exists?
   │          │
  Yes         No
   │          │
   ▼          ▼
Return ID   Create Sensor
              │
              ▼
          Return ID
```
The backend verifies that a sensor UID is not incorrectly associated with another device

### 📊 Measurement Flow
After sensors are registered: 
```
Sensor
   │
   ▼
Read Data
   │
   ▼
Create Measurement
   │
   ▼
ESP32 ApiClient
   │
   ▼
FastAPI Backend
   │
   ▼
Validate Device and Sensor
   │
   ▼
PostgreSQL
```
A single measurement batch can contain measurements from multiple sensors. 

For example: 
```
ESP32
│
├── DHT Sensor
│   ├── temperature
│   └── humidity
│
└── Distance Sensor
    └── distance
```

## 📋 Current ESP32 Features
- [x] Wi-Fi connection
- [x] HTTP communication with FastAPI
- [x] JSON API requests
- [x] Abstract Sensor interface
- [x] Fake DHT Sensor
- [x] Fake Distance Sensor
- [x] Automatic sensor registration
- [x] Sending multiple measurements
- [x] Device and sensor validation
- [x] Measurements stored in PostgreSQL

## 🗺️ Development Roadmap
The project is being developed in the following stages:

### Project Setup
- [x] Create GitHub repository
- [x] Set up project structure
- [x] Configure PostgreSQL
- [x] Configure Docker
- [x] Configure FastAPI
- [x] Configure SQLAlchemy
- [x] Configure Alembic

### Backend
- [x] Create FastAPI application
- [x] Create Device model
- [x] Create Sensor model
- [x] Create Measurement model
- [x] Create Device API
- [x] Create Sensor API
- [x] Create Measurement API
- [x] Add Pydantic schemas
- [x] Add API response schemas
- [x] Organize endpoints using routers
- [x] Add database dependency injection
- [x] Add sensor/device ownership validation

### Database
- [x] PostgreSQL database
- [x] Docker configuration
- [x] SQLAlchemy models
- [x] Alembic migrations
- [x] Device to Sensor relationship
- [x] Sensor to Measurement relationship

### ESP32 Firmware
- [x] PlatformIO setup
- [x] Wi-Fi connection
- [x] HTTP API communication
- [x] JSON payloads
- [x] Abstract Sensor interface
- [x] Fake DHT Sensor
- [x] Fake Distance Sensor
- [x] Automatic sensor registration

### Frontend
- [ ] Set up React application
- [ ] Create dashboard layout
- [ ] Display devices 
- [ ] Display sensors
- [ ] Display latest measurements
- [ ] Create charts for historical measurements
- [ ] Add device management
- [ ] Add admin functionality
- [ ] Add device configuration interface

### Security
- [ ] Authentication
- [ ] User accounts
- [ ] Admin role
- [ ] Device Authentication
- [ ] API authorization
- [ ] Secure device registration

## 📈 Current Status
The backend and ESP32 firmware are currently communicating successfully.

The current data flow is:
```
ESP32
   │
   ├── Sensor Registration
   │
   └── Measurement Submission
            │
            ▼
        FastAPI API
            │
            ▼
        PostgreSQL
```
Multiple sensors can belong to a single ESP32 device, and each sensor can submit multiple measurements.

The backend validates the relationship between devices and sensors before storing measurements.

The next major step is to continue improving the backend architecture and begin building the React dashboard and admin functionality.

## 👨‍💻 Author

Built as a personal full-stack and IoT portfolio project.