# weather-bridge
Bridge project for sending weather station data to other services.

This project uses Poetry for dependency management.
Install dependencies: poetry install

Running the application:
python -m uvicorn weather_bridge.main:app --reload

Docker build:
sudo docker build --tag weather-bridge:0.1 .

Docker run:
docker run --name "BRIDGE_TEST" -p 8088:80 weather-bridge:0.1

Docker run with parameters:
sudo docker run -e SERVICE_MQTT=True -e MQTT_HOST=192.168.1.33 -e MQTT_PORT=1883 -e MQTT_TOPIC=ws1 -e MQTT_ID=docker1 -e CONVERT_TEMP=True -e CONVERT_SPEED=True -e CONVERT_DEPTH=True -p 8088:80 denisvitez/weather-bridge:0.1.2
