from typing import Optional

from fastapi import FastAPI, Request
from .lib import parse_string_to_key_pair, convert_units_speed, convert_units_temp, convert_units_depth
import os
from paho.mqtt import client as mqtt_client


def init_mqtt(client_id, username, password, broker, port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    if username:
        client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


app = FastAPI()
if os.getenv("SERVICE_MQTT", False):
    client_id = os.getenv("MQTT_ID", None)
    username = os.getenv("MQTT_USERNAME", None)
    password = os.getenv("MQTT_PASSWORD", None)
    broker = os.getenv("MQTT_HOST", None)
    port = os.getenv("MQTT_PORT", None)
    if port:
        port = int(port)
    if not (client_id and broker and port):
        print("MQTT enabled but required settings (MQTT_ID, MQTT_HOST, MQTT_PORT) are not configured.")
    else:
        client_mqtt = init_mqtt(client_id, username, password, broker, port)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/hook")
async def read_item(request: Request):
    print("--- Started with the hook. ---")
    content = await request.body()
    data = parse_string_to_key_pair(content.decode())
    # Convert data units
    if os.getenv("CONVERT_TEMP"):
        print("Temperature conversion is enabled.")
        convert_units_temp(data)
    if os.getenv("CONVERT_SPEED"):
        convert_units_speed(data)
        print("Speed conversion is enabled.")
    if os.getenv("CONVERT_DEPTH"):
        convert_units_depth(data)
        print("Depth conversion is enabled.")
    # Check if MQTT is enabled
    if os.getenv("SERVICE_MQTT", False):
        print("MQTT is enabled")
        try:
            client_mqtt.publish("ws_dev/temp", data["temp"])
            print("MQTT messages sent")
        except (RuntimeError, TypeError, NameError) as err:
            print("Failure with sending to MQTT")
    # Check if ThingsSpeak is enabled
    if os.getenv("SERVICE_TS", False):
        print("ThingSpeak is enabled")
        try:
            print("")
        except (RuntimeError, TypeError, NameError) as err:
            print("Failure with sending to ThingsSpeak")
            print(err)
    print("--- Finished with the hook. ---")
    return {"data": data}
