from fastapi import APIRouter, Request
import os
import requests

from weather_bridge.libraries import (
    parse_string_to_key_pair,
    convert_units_speed,
    convert_units_temp,
    convert_units_depth,
    get_data_dict,
    send_mqtt
)

from weather_bridge.init_mqtt import init_mqtt_client

router = APIRouter()

client_mqtt = init_mqtt_client()
mqtt_topic = os.getenv("MQTT_TOPIC", "ws_bridge")


@router.post("/hook")
async def read_item(request: Request):
    print("--- Started with the hook. ---")

    content = await request.body()
    data = parse_string_to_key_pair(content.decode())

    # Conversions
    if os.getenv("CONVERT_TEMP"):
        convert_units_temp(data)

    if os.getenv("CONVERT_SPEED"):
        convert_units_speed(data)

    if os.getenv("CONVERT_DEPTH"):
        convert_units_depth(data)

    # Output data
    relevant_data = get_data_dict(data)

    # MQTT
    if os.getenv("SERVICE_MQTT") and client_mqtt:
        try:
            send_mqtt(client_mqtt, mqtt_topic, relevant_data)
        except Exception as err:
            print("MQTT sending error:", err)

    # ThingSpeak
    if os.getenv("SERVICE_TS"):
        ts_key = os.getenv("TS_KEY")
        if not ts_key:
            print("TS_KEY missing!")
        else:
            params = {"api_key": ts_key}
            for f in range(1, 6):
                env = f"TS_FIELD{f}"
                if os.getenv(env):
                    params[f"field{f}"] = relevant_data[os.getenv(env)]
            requests.get("https://api.thingspeak.com/update", params=params)

    # Custom service
    if os.getenv("SERVICE_CUSTOM"):
        url = os.getenv("CUSTOM_URL")
        if url:
            requests.post(url, json=relevant_data)

    print("--- Finished with the hook. ---")
    return {"data": data}
