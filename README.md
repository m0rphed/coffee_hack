# coffee_hack

Проект хакатона по анализу данных сети кофеен: backend считает клиентские метрики и RFM-сегментацию, frontend показывает аналитические дашборды.

## Что в репозитории

- `api/` - FastAPI API + аналитика на `pandas`.
- `frontend-baggins/` - React-интерфейс с графиками (`Recharts`, `Bootstrap`).
- `*.ipynb` - исследовательские ноутбуки с метриками.

## Основные возможности

Расчет клиентских метрик:
- `total_orders`
- `total_items`
- `avg_order_size`
- `avg_order_interval`
- `unique_items`
- `last_order_date`
- `preferred_time_of_day`
- `preferred_weekday`
- `preferred_hour`
- Поиск часто покупаемых вместе товаров (`products/most_frequent_pairs`).
- RFM-сегментация клиентов (`rfm/status`).
- Расчет персональной скидки по RFM (`rfm/discount`).

## Требования

- Python `3.12+`
- Node.js `18+`
- npm `9+`
- Docker (опционально, для контейнерного запуска API)

## Быстрый старт

### 1) Backend (локально)

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Заполните `api/.env`:

```env
DATASET_CSV_FILE=C:\absolute\path\to\dataset.csv
DB_PATH=C:\absolute\path\to\metrics_db.db
DATA_DIR=C:\absolute\path\to\data
```

Запуск API:

```powershell
uvicorn coffee_hack_api.main:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```

Документация API (Swagger): `http://localhost:8000/docs`

### 2) Backend (Docker)

```powershell
cd api
Copy-Item .env.example .env
```

Для Docker используйте такие значения в `.env`:

```env
DATASET_CSV_FILE=/app/data/hakaton.csv
DB_PATH=/app/data/metrics_db.db
DATA_DIR=/app/data
```

Положите датасет в `api/data/hakaton.csv`, затем запустите:

```powershell
.\rebuild_container.ps1
```

Linux/macOS:

```bash
./rebuild_container.sh
```

### 3) Frontend

```powershell
cd frontend-baggins
npm install
npm start
```

Frontend будет доступен на `http://localhost:3000`.

## Обязательные колонки в CSV

Backend ожидает как минимум эти поля:

- `id`
- `create_datetime`
- `customer_id`
- `order_id`
- `entity_id`

## API endpoints

- `GET /customer/all_metrics` - все клиентские метрики из SQLite-кэша.
- `GET /customer/{customer_id}` - метрики конкретного клиента.
- `POST /admin/rebuild_customer_cache` - пересборка кэша метрик.
- `POST /admin/clear_cache` - очистка кэша.
- `POST /admin/upload_csv` - загрузка CSV в `DATA_DIR`.
- `GET /products/most_frequent_pairs` - частые пары товаров.
- `GET /rfm/status` - RFM-статусы клиентов.
- `GET /rfm/discount` - расчет скидок по RFM.

## Известные ограничения текущей версии

- Часть графиков во frontend использует мок-данные, а не ответы backend.
- В `frontend-baggins/src/pages/oneUserPage.jsx` есть запрос к `http://158.255.6.113:8000/customer/time_of_day_preference/{id}` - такого endpoint в текущем локальном backend нет.

## Лицензия

MIT (см. `LICENSE`).
