# Use an official Python runtime as an image
FROM python:3.9

EXPOSE 80

COPY . /docker_app

WORKDIR /docker_app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD ["uvicorn", "weather_bridge.main:app", "--host", "0.0.0.0", "--port", "80"]
