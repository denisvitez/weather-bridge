from weather_bridge import __version__
from fastapi import APIRouter
import os
from weather_bridge.init_mqtt import client_mqtt

router = APIRouter()


@router.get("/health")
def full_health():
    """Return full service health including MQTT and environment."""

    mqtt_enabled = bool(os.getenv("SERVICE_MQTT"))
    mqtt_connected = client_mqtt.is_connected() if (mqtt_enabled and client_mqtt) else False

    return {
        "status": "ok",
        "version": __version__,
        "service": "weather-bridge",
        "mqtt": {
            "enabled": mqtt_enabled,
            "connected": mqtt_connected,
            "host": os.getenv("MQTT_HOST"),
            "port": os.getenv("MQTT_PORT"),
            "client_id": os.getenv("MQTT_ID")
        },
        "thingspeak": {
            "enabled": bool(os.getenv("SERVICE_TS")),
            "api_key_set": bool(os.getenv("TS_KEY"))
        },
        "custom_service": {
            "enabled": bool(os.getenv("SERVICE_CUSTOM")),
            "url": os.getenv("CUSTOM_URL")
        },
        "converters": {
            "temperature": bool(os.getenv("CONVERT_TEMP")),
            "speed": bool(os.getenv("CONVERT_SPEED")),
            "depth": bool(os.getenv("CONVERT_DEPTH"))
        }
    }
