# Use a more comprehensive base image
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pymongo>=4.6.0
RUN pip install pymongo>=4.6.0

# Copy application files
COPY backend.py . 
COPY skills_embeddings.json .

# Expose the port
EXPOSE 8000

# Use uvicorn to run the application
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]
