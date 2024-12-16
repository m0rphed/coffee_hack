from fastapi import FastAPI, Depends, Query
import pandas as pd
from typing import List, Dict, Optional

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

# загружаем .env файл с указанием пути к .csv
load_dotenv()

CSV_FILE_PATH = os.environ.get("DATASET_CSV_FILE")
if CSV_FILE_PATH is None:
    raise RuntimeError(f"Ошибка загрузки датасета из .csv: '{CSV_FILE_PATH}'")

app = FastAPI()

DATAFRAME_CACHE: pd.DataFrame = None
CUSTOMER_METRICS_CACHE: pd.DataFrame = None


# === Helper function to load data ===
def get_data() -> pd.DataFrame:
    global DATAFRAME_CACHE
    if DATAFRAME_CACHE is None:
        DATAFRAME_CACHE = load_data(CSV_FILE_PATH)
    return DATAFRAME_CACHE


# === Helper function to calculate and cache customer metrics ===
def get_customer_metrics() -> pd.DataFrame:
    global CUSTOMER_METRICS_CACHE
    if CUSTOMER_METRICS_CACHE is None:
        data_df = get_data()
        total_orders = calculate_total_orders(data_df)
        total_items = calculate_total_items(data_df)
        avg_order_size = calculate_avg_order_size(data_df)
        avg_order_interval = calculate_avg_order_interval(data_df)
        unique_items = calculate_unique_items(data_df)
        last_order_date = calculate_last_order_date(data_df)
        time_of_day_preference = calculate_time_of_day_preference(data_df)
        weekday_and_hour_distribution = calculate_weekday_and_hour_distribution(data_df)

        CUSTOMER_METRICS_CACHE = (
            total_orders.merge(total_items, on="customer_id")
            .merge(avg_order_size, on="customer_id")
            .merge(avg_order_interval, on="customer_id")
            .merge(unique_items, on="customer_id")
            .merge(last_order_date, on="customer_id")
            .merge(time_of_day_preference, on="customer_id")
            .merge(weekday_and_hour_distribution, on="customer_id")
        )
    return CUSTOMER_METRICS_CACHE


# === Endpoints for customer metrics ===
@app.get("/customer/all_metrics")
async def all_metrics() -> List[Dict]:
    metrics = get_customer_metrics()
    return metrics.to_dict(orient="records")


@app.get("/customer/total_orders/{customer_id}")
async def total_orders(customer_id: int) -> Dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "total_orders"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/total_items/{customer_id}")
async def total_items(customer_id: int) -> Dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "total_items"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/avg_order_size/{customer_id}")
async def avg_order_size(customer_id: int) -> Dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "avg_order_size"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/avg_order_interval/{customer_id}")
async def avg_order_interval(customer_id: int) -> Dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "avg_order_interval"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/unique_items/{customer_id}")
async def unique_items(customer_id: int) -> Dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "unique_items"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/last_order_date/{customer_id}")
async def last_order_date(customer_id: int) -> dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "last_order_date"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/time_of_day_preference/{customer_id}")
async def time_of_day_preference(customer_id: int) -> dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id, ["customer_id", "preferred_time_of_day"]
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


@app.get("/customer/weekday_and_hour_distribution/{customer_id}")
async def weekday_and_hour_distribution(customer_id: int) -> Dict:
    metrics = get_customer_metrics()
    result = metrics.loc[
        metrics["customer_id"] == customer_id,
        ["customer_id", "preferred_weekday", "preferred_hour"],
    ]
    return result.to_dict(orient="records")[0] if not result.empty else {}


# === Endpoints for product analysis ===
@app.get("/products/buy_together")
async def products_bought_together() -> list[dict]:
    data = get_data()
    result = buy_together(data)
    return result.to_dict(orient="records")


@app.get("/products/popular_products_of_the_day")
async def popular_products_of_the_day_(
    day_date: int, month_date: int, year_date: int
) -> list[dict]:
    data = get_data()
    result = popular_products_of_the_day(data, day_date, month_date, year_date)
    return result.to_dict(orient="records")


@app.get("/products/most_frequent_pairs")
async def most_frequent_pairs(customer_id: Optional[int] = Query(None)) -> list[dict]:
    data = get_data()
    result = find_most_frequent_pairs(data, customer_id)
    return result.to_dict(orient="records")


# === Endpoints for RFM analysis ===
@app.get("/rfm/status")
async def rfm_status() -> list[dict]:
    data = get_data()
    result = prepare_rfm(data)
    result["rfm_status"] = result["RFM_score"].apply(assign_rfm_status)
    return result.to_dict(orient="records")


@app.get("/rfm/discount")
async def rfm_discount() -> list[dict]:
    data = get_data()
    result = prepare_rfm(data)
    result["discount"] = result.apply(
        lambda row: calculate_discount(row["R_rank"], row["F_rank"], row["M_rank"]),
        axis=1,
    )
    return result.to_dict(orient="records")


@app.get("/rfm/full")
async def rfm_full() -> list[dict]:
    data = get_data()
    result = prepare_rfm(data)
    result["rfm_status"] = result["RFM_score"].apply(assign_rfm_status)
    result["discount"] = result.apply(
        lambda row: calculate_discount(row["R_rank"], row["F_rank"], row["M_rank"]),
        axis=1,
    )
    return result.to_dict(orient="records")


if __name__ == "__main__":
    # Вычисляем метрики клиентов
    customer_metrics = get_customer_metrics()
    print("Метрики клиентов")
    print(customer_metrics.head())
