# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y netcat-openbsd gcc default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Make wait-for-db.sh executable
RUN chmod +x wait-for-db.sh

# Expose Flask port
EXPOSE 8000

# Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8000

# Run Flask through wait-for-db.sh
CMD ["./wait-for-db.sh", "db", "flask", "run", "--host=0.0.0.0", "--port=8000"]
