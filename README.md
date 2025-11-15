🌤️ weather-bridge

weather-bridge is a lightweight bridge service that collects weather station data and forwards it to other services such as MQTT brokers and HTTP endpoints.
It is designed to run on minimal hardware and supports Docker deployment for easy integration.

📦 Docker Image

Official container image:

👉 Docker Hub:
https://hub.docker.com/repository/docker/denisvitez/weather-bridge

📚 Installation (virtualenv + pip)
1️⃣ Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt

🚀 Running the Application Locally

Start the FastAPI service using Uvicorn:

python -m uvicorn weather_bridge.main:app --reload


The API will run on:

http://localhost:8000

⚙️ Environment Variables \
📡 Service Toggles

| Variable         | Default | Description                                    |
| ---------------- | ------- | ---------------------------------------------- |
| `SERVICE_MQTT`   | `False` | Enable sending weather data to an MQTT broker. |
| `SERVICE_TS`     | `False` | Enable sending data to ThingSpeak over HTTP.   |
| `SERVICE_CUSTOM` | `False` | Enable sending data to a custom HTTP endpoint. |
📨 MQTT Settings

| Variable        | Default     | Description                                              |
| --------------- | ----------- | -------------------------------------------------------- |
| `MQTT_HOST`     | `None`      | Hostname or IP of the MQTT broker.                       |
| `MQTT_PORT`     | `1883`      | Port number of the broker.                               |
| `MQTT_ID`       | *Random*    | Optional client ID. Random ID is used in anonymous mode. |
| `MQTT_USERNAME` | `None`      | MQTT username (optional).                                |
| `MQTT_PASSWORD` | `None`      | MQTT password (optional).                                |
| `MQTT_TOPIC`    | `ws_bridge` | Topic where parsed data will be published.               |
🌐 ThingSpeak Settings

| Variable    | Default | Description                                        |
| ----------- | ------- | -------------------------------------------------- |
| `TS_KEY`    | `None`  | ThingSpeak API key. Required if `SERVICE_TS=True`. |
| `TS_FIELD1` | `None`  | Map parsed key → ThingSpeak field1.                |
| `TS_FIELD2` | `None`  | Map parsed key → ThingSpeak field2.                |
| `TS_FIELD3` | `None`  | Map parsed key → ThingSpeak field3.                |
| `TS_FIELD4` | `None`  | Map parsed key → ThingSpeak field4.                |
| `TS_FIELD5` | `None`  | Map parsed key → ThingSpeak field5.                |
🔗 Custom Hook Settings

| Variable     | Default | Description                                    |
| ------------ | ------- | ---------------------------------------------- |
| `CUSTOM_URL` | `None`  | URL to POST the parsed weather data to (JSON). |
🔧 Data Conversion Settings

| Variable        | Default | Description                                |
| --------------- | ------- | ------------------------------------------ |
| `CONVERT_TEMP`  | `False` | Convert temperature units (e.g., °F → °C). |
| `CONVERT_SPEED` | `False` | Convert wind speed units.                  |
| `CONVERT_DEPTH` | `False` | Convert rainfall/depth units.              |

🛠️ Docker
🔨 Build the Docker Image
sudo docker build --tag weather-bridge:0.1.2 .

▶️ Run the Container
docker run --name "BRIDGE_TEST" -p 8088:80 weather-bridge:0.1.2

▶️ Run with Environment Parameters
sudo docker run \
  -e SERVICE_MQTT=True \
  -e MQTT_HOST=192.168.1.40 \
  -e MQTT_PORT=1883 \
  -e MQTT_TOPIC=ws1 \
  -e CONVERT_TEMP=True \
  -e CONVERT_SPEED=True \
  -e CONVERT_DEPTH=True \
  -p 8088:80 \
  denisvitez/weather-bridge:0.1.2
