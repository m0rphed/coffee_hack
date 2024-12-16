# rebuild.ps1
# PowerShell-скрипт для пересборки
#   и перезапуска Docker-контейнера

# Название Docker-контейнера и образа
$CONTAINER_NAME = "coffee_api_container"
$IMAGE_NAME = "coffee_api_image"

Write-Host "Stopping existing container..."
# Остановка и удаление старого контейнера
if (docker ps -q --filter "name=$CONTAINER_NAME") {
    docker stop $CONTAINER_NAME | Out-Null
    docker rm $CONTAINER_NAME | Out-Null
}

Write-Host "Building Docker image..."
# Пересборка образа
docker build -t $IMAGE_NAME .

Write-Host "Starting new container..."
# Запуск нового контейнера с переменными окружения и монтированием данных
docker run -d --name $CONTAINER_NAME `
  --env-file .env `
  -p 8000:8000 `
  -v "$((Get-Location).Path)/data:/app/data" `
  $IMAGE_NAME

Write-Host "Container restarted successfully!"


# .env
# Пример переменных окружения
# DB_URL=sqlite:///data/metrics_db.db
# API_KEY=secret_key_example
# DEBUG=true
