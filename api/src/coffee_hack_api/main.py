import sqlite3
import pandas as pd
from fastapi import FastAPI, Query, File, UploadFile
from typing import List, Dict, Optional
from pprint import pprint

from coffee_hack_api.analysis.prepare import load_data
from coffee_hack_api.analysis.customer_metrics import (
    calculate_total_orders,
    calculate_total_items,
    calculate_avg_order_size,
    calculate_avg_order_interval,
    calculate_unique_items,
    calculate_last_order_date,
    calculate_time_of_day_preference,
    calculate_weekday_and_hour_distribution,
)

from coffee_hack_api.analysis.products_most_relevant import (
    buy_together,
    popular_products_of_the_day,
    find_most_frequent_pairs,
)

from coffee_hack_api.analysis.rfm import (
    prepare_rfm,
    assign_rfm_status,
    calculate_discount,
)

# загрузка пути
from dotenv import load_dotenv
import os


def _loading_envs() -> tuple[str, str]:
    # загружаем .env файл с указанием пути к .csv
    load_dotenv()

    csv_file_path = os.environ.get("DATASET_CSV_FILE")
    print("[info] Путь к .csv файлу", csv_file_path)
    if csv_file_path is None:
        raise RuntimeError(f"Ошибка загрузки датасета из .csv: '{csv_file_path}'")

    db_path = os.environ.get("DB_PATH")
    print("[info] Путь к .db файлу", db_path)
    if db_path is None:
        raise RuntimeError(f"Ошибка загрузки SQLite БД из .csv: '{db_path}'")

    return csv_file_path, db_path


CSV_FILE_PATH, DB_PATH = _loading_envs()

app = FastAPI()


# === Инициализация базы данных SQLite ===
def initialize_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS customer_metrics (
            customer_id INTEGER PRIMARY KEY,
            total_orders INTEGER,
            total_items INTEGER,
            avg_order_size REAL,
            avg_order_interval REAL,
            unique_items INTEGER,
            last_order_date TEXT,
            preferred_time_of_day INTEGER,
            preferred_weekday INTEGER,
            preferred_hour INTEGER
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS products_buy_together (
            product_1 INTEGER,
            product_2 INTEGER,
            support REAL,
            PRIMARY KEY (product_1, product_2)
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS rfm_metrics (
            customer_id INTEGER PRIMARY KEY,
            recency_score INTEGER,
            frequency_score INTEGER,
            monetary_score INTEGER,
            rfm_score TEXT,
            rfm_status TEXT,
            discount REAL
        );
        """)


# === Обновить кэш данных в базе SQLite ===
def rebuild_customer_metrics_cache(file_path: str):
    data = load_data(file_path)

    total_orders = calculate_total_orders(data)
    total_items = calculate_total_items(data)
    avg_order_size = calculate_avg_order_size(data)
    avg_order_interval = calculate_avg_order_interval(data)
    unique_items = calculate_unique_items(data)
    last_order_date = calculate_last_order_date(data)
    time_of_day_preference = calculate_time_of_day_preference(data)
    weekday_and_hour_distribution = calculate_weekday_and_hour_distribution(data)

    customer_metrics = (
        total_orders.merge(total_items, on="customer_id")
        .merge(avg_order_size, on="customer_id")
        .merge(avg_order_interval, on="customer_id")
        .merge(unique_items, on="customer_id")
        .merge(last_order_date, on="customer_id")
        .merge(time_of_day_preference, on="customer_id")
        .merge(weekday_and_hour_distribution, on="customer_id")
    )

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM customer_metrics")
        customer_metrics.to_sql(
            "customer_metrics", conn, if_exists="replace", index=False
        )


# === Доступ к данным из SQLite ===
def get_customer_metrics_from_db() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query("SELECT * FROM customer_metrics", conn)
    return df


# === Получить данные для конкретного клиента ===
def get_customer_metrics_by_id(customer_id: int) -> Dict:
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT * FROM customer_metrics WHERE customer_id = ?"
        result = pd.read_sql_query(query, conn, params=(customer_id,))
    return result.to_dict(orient="records")[0] if not result.empty else {}


# === Эндпоинты для работы с SQLite кэшем ===
@app.get("/customer/all_metrics")
async def all_metrics() -> List[Dict]:
    metrics = get_customer_metrics_from_db()
    result = metrics.to_dict(orient="records")
    pprint(result)
    return result


@app.get("/customer/{customer_id}")
async def customer_metrics(customer_id: int) -> Dict:
    result = get_customer_metrics_by_id(customer_id)
    pprint(result)
    return result


@app.post("/admin/rebuild_customer_cache")
async def rebuild_customer_cache(file_path: Optional[str] = None) -> Dict:
    try:
        if file_path is None:
            file_path = CSV_FILE_PATH
        rebuild_customer_metrics_cache(CSV_FILE_PATH)
        return {
            "status": "success",
            "message": "Customer metrics cache rebuilt successfully.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/admin/clear_cache")
async def clear_cache() -> Dict:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM customer_metrics")
        return {"status": "success", "message": "Cache cleared successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/admin/upload_csv")
async def upload_csv(file: UploadFile = File(...)) -> Dict:
    try:
        data_dir = os.environ.get("DATA_DIR")
        if data_dir is None:
            raise RuntimeError("Переменная окружения DATA_DIR не была заданна")

        filename = "hakaton.csv" if file.filename is None else file.filename
        file_path = os.path.join(data_dir, filename)

        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return {
            "status": "success",
            "message": f"File {file.filename} uploaded successfully.",
            "file_path": file_path,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/products/most_frequent_pairs")
async def most_frequent_pairs(customer_id: Optional[int] = Query(None)) -> List[Dict]:
    data = load_data(CSV_FILE_PATH)
    df_buy_together = buy_together(data)
    result = find_most_frequent_pairs(df_buy_together, customer_id)
    pprint(result.to_dict(orient="records"))
    return result.to_dict(orient="records")


@app.get("/rfm/status")
async def rfm_status() -> List[Dict]:
    data = load_data(CSV_FILE_PATH)
    result = prepare_rfm(data)
    result["rfm_status"] = result["RFM_score"].apply(assign_rfm_status)
    pprint(result.to_dict(orient="records"))
    return result.to_dict(orient="records")


@app.get("/rfm/discount")
async def rfm_discount() -> List[Dict]:
    data = load_data(CSV_FILE_PATH)
    result = prepare_rfm(data)
    result["discount"] = result.apply(
        lambda row: calculate_discount(row["R_rank"], row["F_rank"], row["M_rank"]),
        axis=1,
    )
    pprint(result.to_dict(orient="records"))
    return result.to_dict(orient="records")


# === Инициализация базы данных при запуске ===
if __name__ == "__main__":
    initialize_db()
    print("SQLite база инициализирована.")
