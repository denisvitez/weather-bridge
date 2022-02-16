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