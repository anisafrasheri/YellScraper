# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir selenium apify-client

# Set environment variable for Apify
ENV PYTHONUNBUFFERED=1

# Command to run
CMD ["python", "main.py"]
