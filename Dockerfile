FROM python:3.9

# Установка всех зависимостей в одном RUN слое
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
        fastapi==0.110.0 \
        uvicorn[standard]==0.31.1 \
        websockets==12.0 \
        sqlalchemy==2.0.28 \
        psycopg2-binary==2.9.9 \
        python-dotenv==1.0.1 \
        redis==5.0.1 \
        python-telegram-bot==21.1.1 \
        pydantic-settings==2.2.1 \
        pydantic==2.7.1

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

COPY src /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]