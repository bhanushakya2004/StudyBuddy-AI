# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PORT=8080 \
    WORKDIR=/app

# Set the working directory inside the container
WORKDIR $WORKDIR

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first (for efficient Docker caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# List the /app directory for debugging
RUN ls -l /app

# Expose the required port
EXPOSE 8080

# Set default command to run FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
