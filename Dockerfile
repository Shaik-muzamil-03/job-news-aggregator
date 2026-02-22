# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY README.md .
COPY src ./src

# Install Python dependencies
RUN pip install --upgrade pip && pip install -e .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
