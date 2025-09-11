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

# Install Python dependencies
RUN if [ -f requirements.txt ]; then \
        uv pip install --system -r requirements.txt; \
    elif [ -f pyproject.toml ]; then \
        uv pip install --system -e .; \
    else \
        echo "No requirements file found"; \
    fi

# Copy the application code
COPY . .

# Install the package if pyproject.toml exists
RUN if [ -f pyproject.toml ]; then uv pip install --system -e .; fi

# Expose the port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
