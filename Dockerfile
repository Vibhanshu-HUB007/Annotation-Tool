# Dockerfile for root-level build (when root directory is set to project root)
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies only for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY backend/requirements-minimal.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage - minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy only installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY backend/ ./backend/

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
ENV PORT=8000
EXPOSE $PORT

# Run the application
WORKDIR /app/backend
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
