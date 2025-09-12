# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster Python package management
RUN pip install uv

# Copy requirements first for better caching
COPY requirements.txt* pyproject.toml* setup.py* ./

# Install essential packages first
RUN uv pip install --system fastapi uvicorn[standard] dramatiq redis

# Install Python dependencies from requirements if it exists
RUN if [ -f requirements.txt ]; then \
        uv pip install --system -r requirements.txt; \
    else \
        echo "No requirements.txt found, will install from pyproject.toml"; \
    fi

# Copy the application code
COPY . .

# Install the package in development mode, ignoring setup issues
RUN if [ -f pyproject.toml ]; then \
        uv pip install --system --no-deps -e . || \
        echo "Package installation failed, but dependencies should be available"; \
    fi

# Set Python path to ensure modules can be found
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
