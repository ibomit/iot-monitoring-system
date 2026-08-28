# IoT Monitoring System 

An IoT monitoring system designed to collect sensor data from ESP32 devices and display it through a web-based dashboard.

The Project is currently under development and is being built step by step as a full-stack IoT application.

## 🎯 Project Goals

The main goal of this project is to build a complete IoT monitoring system that can: 

- Collect sensor data from ESP32 devices
- Sens sensor readings to a backend API
- Store sensor data in a database 
- Display sensor readings in a web dashboard
- Monitor multiple devices and rooms 
- Visualize sensor activity and movement 

## 🏗️ Project Architecture

The planned architecture is: 
```
ESP32 / Simulator
        │
        │ HTTP + JSON
        ▼
   FastAPI Backend
        │
        | SQLAlchemy
        ▼
PostgreSQL Database
        │
        ▼
 React Frontend
 ```
 During development, a Python simulator will initially be used to simulate ESP32 sensor data.

## 📁 Project Structure

```iot-monitoring-system/
│
├── backend/       # FastAPI backend application
├── docs/          # Project documentation
├── firmware/      # ESP32 firmware
├── frontend/      # React web dashboard
├── simulator/     # Sensor/ESP32 simulator
│
├── README.md
└── .gitignore
```
## 🛠️ Current Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- uv
- PostgreSQL

### Planned
- React
- JavaScript
- ESP32
- PlatformIO or Arduino framework

## ⚙️ Backend Setup

´´´
cd backend
´´´
Run the FastAPI development server:
```
uv run fastapi dev app/main.py 
```
or 
```
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
## Current API Endpoints
### Health Check 
```
GET /health
```
Example response: 
```
{
    "status": "ok"
}
```
### Submit Sensor Reading
```
POST /api/readings
```
Stores the reading in PostgreSQL.
Example request:
```
{
    "device_id": "simulator-001",
    "temperature": "22.5",
    "humidity": 48
}
```
Example response:
```
{
    "message": "Reading received",
    "data": {
        "device_id": "simulator-001",
        "temperature": 22.5,
        "humidity": 48
    }
}
```
### Get Sensor Readings
```
GET /api/readings
```
Returns all sensor readings currently stored in the database.
Example response:
```
[
    {
        "id": "simulator-001",
        "temperature": 22.5,
        "humidity": 48.0,
        "created_at": "2026-08-28T20:00:00"
    },
    {
        "id": "simulator-001",
        "temperature": 24.5,
        "humidity": 39.0,
        "created_at": "2026-08-28T20:01:00"
    },
]
```
## 🤖 Sensor Simulator
A Python-based sensor simulator is used during development to simulate an IoT device before connecting the real ESP32 hardware.
The simulator generates random sensor readings and sens them to the FastAPI backend every 5 seconds.

### Simulated Data
The simulator currently generates: 
- Temperature between 18°C and 30°C
- Humidity between 30% and 70%
- Device ID: `simulator-001`

### Running the Simulator
Make sure the FastAPI backend is running first:
```
cd backend
uv run fastapi dev app/main.py
```
Then, in a separate terminal, run the simulator:
```
cd backend
uv run python ../simulator/sensor_simulator.py
```
Example output:
```
Sent: {'device_id': 'simulator-001', 'temperature': 24.31, 'humidity': 53.72}
Server response: {'message': 'Reading received'}
```


## 🗄️ Database
The Project uses PostgreSQL to store sensor readings.
PostgreSQL runs inside a Docker container.
### Database Stack
- PostgreSQL
- Docker
- SQLAlchemy
- psycopg
### Running the Database
To run the database, start the docker container.
``` docker compose up -d ```
To stop the container you can run 
``` docker compose down ```  
Current development database configuration:
```
Database: iot_db
Username: iot_user
Password: iot_password
Host: localhost
Port: 5432
```
The current credentials are intended for local development only. Environment variables will be used for sensitive configuration in later stages of the project.

## ⚙️ ESP32 Firmware
The project includes firmware for an ESP32 microcontroller, located in the `firmware/` directory.

The ESP32 firmware is developed using:
- PlatformIO
- Arduino framework
- Espressif ESP32 platform

### Hardware Setup
The ESP32 development board is connected to the development machine via USB and is detected as: 
```
/dev/ttyUSB0
```

### Firmware Development
The firmware project is configured as a PlatformIO project.

Current configuration:
```
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino

monitor_speed = 115200
upload_port = /dev/ttyUSB0
monitor_port = /dev/ttyUSB0 
```
### First Firmware Test
The initial firmware test verifies that:
- PlatformIO can build the ESP32 firmware
- Firmware can successfully be uploaded to the ESP32
- Serial communication works correctly
The test program sends messages through the serial connection at ```115200``` baud.

### End-to-End ESP32 Communication

The ESP32 can connect to Wi-Fi and send sensor readings to the FastAPI backend using HTTP 

### Data Flow
ESP32 -> Wi-Fi -> FastApi -> PostgreSQL 

## 🗺️ Development Roadmap
The project is being developed in the following stages:

- [x] Create GitHub repository
- [x] Set up project structure
- [x] Set up FastAPI backend
- [x] Create health check endpoint
- [x] Create sensor readings API endpoint
- [x] Create Python sensor simulator
- [x] Store sensor readings in a database
- [x] Connect ESP32 to the backend
- [ ] Build React dashboard
- [ ] Add room visualization
- [ ] Add movement detection visualization
- [ ] Improve UI and add data visualization

## 📈 Current Status
The FastAPI backend is currently running and can receive sensor readings through the REST API.

The next step is to create a Python simulator that generates sensor data and sends it to the backend.

## 👨‍💻 Author

Built as a personal full-stack and IoT portfolio project.