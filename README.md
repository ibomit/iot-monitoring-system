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
        ▼
    Database
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

### Planned
- PostgreSQL
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
## 🗺️ Development Roadmap

The project is being developed in the following stages:

- [x] Create GitHub repository
- [x] Set up project structure
- [x] Set up FastAPI backend
- [x] Create health check endpoint
- [x] Create sensor readings API endpoint
- [ ] Create Python sensor simulator
- [ ] Store sensor readings in a database
- [ ] Connect ESP32 to the backend
- [ ] Build React dashboard
- [ ] Add room visualization
- [ ] Add movement detection visualization
- [ ] Improve UI and add data visualization

## 📈 Current Status
The FastAPI backend is currently running and can receive sensor readings through the REST API.

The next step is to create a Python simulator that generates sensor data and sends it to the backend.

## 👨‍💻 Author

Built as a personal full-stack and IoT portfolio project.