import os
import uuid
from paho.mqtt import client as mqtt_client

client_mqtt = None

def init_mqtt(p_broker, p_port):
    def on_connect(cli, userdata, flags, rc):
        print(f"[MQTT] on_connect rc={rc}")

    def on_disconnect(cli, userdata, rc):
        print(f"[MQTT] Disconnected rc={rc}. Reconnecting...")
        try:
            cli.reconnect()
        except Exception as e:
            print("[MQTT] reconnect error:", e)

    # Generate a random anonymous client ID
    random_id = "wb-" + uuid.uuid4().hex[:10]
    print("[MQTT] Using random client_id:", random_id)

    client = mqtt_client.Client(client_id=random_id, clean_session=True)

    # Anonymous mode
    client.username_pw_set(None, None)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.reconnect_delay_set(1, 30)

    client.connect(p_broker, p_port)
    client.loop_start()

    return client

def init_mqtt_client():
    global client_mqtt

    broker = os.getenv("MQTT_HOST")
    port = int(os.getenv("MQTT_PORT"))

    client_mqtt = init_mqtt(broker, port)
    return client_mqtt
