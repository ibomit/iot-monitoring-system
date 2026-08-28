from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SensorReading(BaseModel):
    device_id: str
    temperature: float
    humidity: float




# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/sensor_readings")
def create_reading(reading: SensorReading):
    return {
        "message": "Reading received", 
        "data": reading
    }