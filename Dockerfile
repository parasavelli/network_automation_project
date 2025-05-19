# Dockerfile for SSH Config Collector

FROM python:3.11-slim

WORKDIR /app

# Copy source and configuration files
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/
COPY requirements.txt .
COPY requirements-dev.txt .

# Install runtime dependencies only
RUN pip install --no-cache-dir -r requirements.txt

# Entry point for CLI execution
ENTRYPOINT ["python", "scripts/run_ssh_backup.py"]
