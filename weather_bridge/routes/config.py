from fastapi import APIRouter
from weather_bridge.libraries import add_env_to_dict

router = APIRouter()

@router.get("/config")
def get_config():
    data = {}

    # Services
    add_env_to_dict(data, "SERVICE_MQTT")
    add_env_to_dict(data, "SERVICE_TS")
    add_env_to_dict(data, "SERVICE_CUSTOM")

    # MQTT
    for key in ["MQTT_HOST", "MQTT_PORT", "MQTT_ID", "MQTT_USERNAME", "MQTT_PASSWORD", "MQTT_TOPIC"]:
        add_env_to_dict(data, key, key == "MQTT_PASSWORD")

    # ThingSpeak
    for key in ["TS_KEY", "TS_FIELD1", "TS_FIELD2", "TS_FIELD3", "TS_FIELD4", "TS_FIELD5"]:
        add_env_to_dict(data, key)

    # Converters
    add_env_to_dict(data, "CONVERT_TEMP")
    add_env_to_dict(data, "CONVERT_SPEED")
    add_env_to_dict(data, "CONVERT_DEPTH")

    return data
