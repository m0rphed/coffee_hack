# Dockerfile
# Используем Python образ с питоном 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем git для поддержки editable пакетов
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости для работы с переменными окружения
RUN pip install python-dotenv

# Скопируем зависимости
COPY README.md pyproject.toml requirements.txt ./

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируем исходники приложения
COPY src ./src
COPY data ./data
COPY .env ./

# Устанавливаем рабочую директорию на каталог с API
WORKDIR /app/src

# Команда запуска FastAPI через uvicorn
CMD ["uvicorn", "coffee_hack_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]