#!/bin/bash

# Название Docker-контейнера и образа
CONTAINER_NAME="coffee_api_container"
IMAGE_NAME="coffee_api_image"

# Остановка и удаление старого контейнера
echo "Stopping existing container..."
docker stop $CONTAINER_NAME 2>/dev/null
docker rm $CONTAINER_NAME 2>/dev/null

# Пересборка образа
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Запуск нового контейнера с переменными окружения и монтированием данных
echo "Starting new container..."
docker run -d --name $CONTAINER_NAME \
  --env-file .env \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  $IMAGE_NAME

echo "Container restarted successfully!"


# .env
# Пример переменных окружения
# DB_URL=sqlite:///data/metrics_db.db
# API_KEY=secret_key_example
# DEBUG=true
