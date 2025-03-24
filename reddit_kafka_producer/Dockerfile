# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9092 available to the world outside this container (optional if using Kafka)
EXPOSE 9092

# Define environment variables (optional, can be configured at runtime)
ENV KAFKA_BROKER=localhost:9092

# Run producer.py when the container launches
CMD ["python", "producer.py"]