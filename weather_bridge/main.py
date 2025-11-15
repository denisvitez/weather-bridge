from fastapi import FastAPI
from weather_bridge.init_mqtt import init_mqtt_client
from weather_bridge.routes.landing import router as landing_router
from weather_bridge.routes.config import router as config_router
from weather_bridge.routes.hook import router as hook_router
from weather_bridge.routes.health import router as health_router

import os

app = FastAPI()

# Initialize MQTT if enabled
client_mqtt = init_mqtt_client()
mqtt_topic = os.getenv("MQTT_TOPIC", "ws_bridge")

# Include routes
app.include_router(landing_router)
app.include_router(config_router)
app.include_router(hook_router)
app.include_router(health_router)

@app.on_event("startup")
async def startup_event():
    print("weather-bridge started successfully.")
