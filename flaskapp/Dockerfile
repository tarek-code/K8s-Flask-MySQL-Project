# Use an official Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY app.py .

# Expose the Flask port
EXPOSE 5002

# Command to run the app
CMD ["python", "app.py"]
