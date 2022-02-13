from typing import Optional

from fastapi import FastAPI, Request
from .lib import \
    parse_string_to_key_pair, \
    convert_units_speed, \
    convert_units_temp, \
    convert_units_depth, \
    add_env_to_dict, \
    get_data_dict, \
    send_mqtt
import os
from paho.mqtt import client as mqtt_client


def init_mqtt(p_client_id, p_username, p_password, p_broker, p_port):
    def on_connect(cli, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(p_client_id)
    if p_username:
        client.username_pw_set(p_username, p_password)
    client.on_connect = on_connect
    client.connect(p_broker, p_port)
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

mqtt_topic = os.getenv("MQTT_TOPIC", "ws_bridge")


@app.get("/config")
def get_config():
    data = dict()
    # Services
    add_env_to_dict(data, "SERVICE_MQTT")
    add_env_to_dict(data, "SERVICE_TS")
    # MQTT settings
    add_env_to_dict(data, "MQTT_HOST")
    add_env_to_dict(data, "MQTT_PORT")
    add_env_to_dict(data, "MQTT_ID")
    add_env_to_dict(data, "MQTT_USERNAME")
    add_env_to_dict(data, "MQTT_PASSWORD", True)
    add_env_to_dict(data, "MQTT_TOPIC")
    # TS settings
    add_env_to_dict(data, "TS_KEY")
    add_env_to_dict(data, "TS_FIELD1")
    add_env_to_dict(data, "TS_FIELD2")
    add_env_to_dict(data, "TS_FIELD3")
    add_env_to_dict(data, "TS_FIELD4")
    add_env_to_dict(data, "TS_FIELD5")
    # Converter settings
    add_env_to_dict(data, "CONVERT_TEMP")
    add_env_to_dict(data, "CONVERT_SPEED")
    add_env_to_dict(data, "CONVERT_DEPTH")
    return data


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
    relevant_data = get_data_dict(data)
    if os.getenv("SERVICE_MQTT", False):
        print("MQTT is enabled")
        try:
            # Send all relevant data
            print(relevant_data)
            send_mqtt(client_mqtt, mqtt_topic, relevant_data)
            print("MQTT messages sent")
        except (RuntimeError, TypeError, NameError) as err:
            print("Failure with sending to MQTT", err)
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
