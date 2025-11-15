# Use Python 3.12 base image
FROM python:3.12-slim

# Expose the API port
EXPOSE 80

# Copy app into the container
COPY . /docker_app

# Set working directory
WORKDIR /docker_app

# Install dependencies using pip + requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Run your FastAPI app
CMD ["uvicorn", "weather_bridge.main:app", "--host", "0.0.0.0", "--port", "80"]
