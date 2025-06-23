FROM python:3.9

WORKDIR /app

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    postgresql-dev \
    curl

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "__main__:app", "--host", "0.0.0.0", "--port", "8000"]