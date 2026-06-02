# Use Python 3.12 base image (matching Prefect Horizon's base)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .
COPY flows.py .

# Expose port
EXPOSE 3000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# Run the FastAPI server
CMD ["python", "server.py"]

# Made with Bob
