#!/bin/bash
set -e

# Установка зависимостей
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Проверка установки websockets
echo "Проверка установки websockets:"
pip show websockets || echo "websockets не установлен!"
python -c "import websockets; print('Версия websockets:', websockets.__version__)" || echo "Ошибка импорта websockets"

# Запуск приложения
exec uvicorn main:app --host 0.0.0.0 --port 8000