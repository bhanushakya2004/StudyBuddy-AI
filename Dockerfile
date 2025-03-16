# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only requirements file first (to leverage Docker caching)
COPY requirements.txt .

# Install dependencies (optimize cache layers)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Set environment variable for Cloud Run
ENV PORT=8080

# Expose the required port
EXPOSE 8080

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
