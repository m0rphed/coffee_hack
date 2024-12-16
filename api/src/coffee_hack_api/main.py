from fastapi import FastAPI, Depends, Query
import pandas as pd
from typing import List, Dict, Optional
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
from coffee_hack_api.analysis.prepare import load_data

app = FastAPI()

DATAFRAME_CACHE: pd.DataFrame = None


# === Helper function to load data ===
def get_data() -> pd.DataFrame:
    global DATAFRAME_CACHE
    if DATAFRAME_CACHE is None:
        DATAFRAME_CACHE = load_data("/mnt/data/hakaton.csv")
    return DATAFRAME_CACHE


# === Endpoints for customer metrics ===
@app.get("/customer/total_orders")
async def total_orders() -> List[Dict]:
    data = get_data()
    result = calculate_total_orders(data)
    return result.to_dict(orient="records")


@app.get("/customer/total_items")
async def total_items() -> List[Dict]:
    data = get_data()
    result = calculate_total_items(data)
    return result.to_dict(orient="records")


@app.get("/customer/avg_order_size")
async def avg_order_size() -> List[Dict]:
    data = get_data()
    result = calculate_avg_order_size(data)
    return result.to_dict(orient="records")


@app.get("/customer/avg_order_interval")
async def avg_order_interval() -> List[Dict]:
    data = get_data()
    result = calculate_avg_order_interval(data)
    return result.to_dict(orient="records")


@app.get("/customer/unique_items")
async def unique_items() -> list[Dict]:
    data = get_data()
    result = calculate_unique_items(data)
    return result.to_dict(orient="records")


@app.get("/customer/last_order_date")
async def last_order_date() -> list[Dict]:
    data = get_data()
    result = calculate_last_order_date(data)
    return result.to_dict(orient="records")


@app.get("/customer/time_of_day_preference")
async def time_of_day_preference() -> list[Dict]:
    data = get_data()
    result = calculate_time_of_day_preference(data)
    return result.to_dict(orient="records")


@app.get("/customer/weekday_and_hour_distribution")
async def weekday_and_hour_distribution() -> list[Dict]:
    data = get_data()
    result = calculate_weekday_and_hour_distribution(data)
    return result.to_dict(orient="records")


# === Endpoints for product analysis ===
@app.get("/products/buy_together")
async def products_bought_together() -> list[Dict]:
    data = get_data()
    result = buy_together(data)
    return result.to_dict(orient="records")


@app.get("/products/popular_products_of_the_day")
async def popular_products_of_the_day(
    day_date: int, month_date: int, year_date: int
) -> list[Dict]:
    data = get_data()
    result = popular_products_of_the_day(data, day_date, month_date, year_date)
    return result.to_dict(orient="records")


@app.get("/products/most_frequent_pairs")
async def most_frequent_pairs(customer_id: Optional[int] = Query(None)) -> list[Dict]:
    data = get_data()
    result = find_most_frequent_pairs(data, customer_id)
    return result.to_dict(orient="records")


# === Endpoints for RFM analysis ===
@app.get("/rfm/status")
async def rfm_status() -> list[Dict]:
    data = get_data()
    result = prepare_rfm(data)
    result["rfm_status"] = result["RFM_score"].apply(assign_rfm_status)
    return result.to_dict(orient="records")


@app.get("/rfm/discount")
async def rfm_discount() -> list[Dict]:
    data = get_data()
    result = prepare_rfm(data)
    result["discount"] = result.apply(
        lambda row: calculate_discount(row["R_rank"], row["F_rank"], row["M_rank"]),
        axis=1,
    )
    return result.to_dict(orient="records")


@app.get("/rfm/full")
async def rfm_full() -> list[Dict]:
    data = get_data()
    result = prepare_rfm(data)
    result["rfm_status"] = result["RFM_score"].apply(assign_rfm_status)
    result["discount"] = result.apply(
        lambda row: calculate_discount(row["R_rank"], row["F_rank"], row["M_rank"]),
        axis=1,
    )
    return result.to_dict(orient="records")


# === Tests ===
def __test_endpoints():
    import requests

    base_url = "http://localhost:8000"
    endpoints = [
        "/customer/total_orders",
        "/customer/total_items",
        "/customer/avg_order_size",
        "/customer/avg_order_interval",
        "/customer/unique_items",
        "/customer/last_order_date",
        "/customer/time_of_day_preference",
        "/customer/weekday_and_hour_distribution",
        "/products/buy_together",
        "/products/popular_products_of_the_day?day_date=1&month_date=1&year_date=2024",
        "/products/most_frequent_pairs",
        "/rfm/status",
        "/rfm/discount",
        "/rfm/full",
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(base_url + endpoint)
            assert (
                response.status_code == 200
            ), f"Endpoint {endpoint} failed with status {response.status_code}"
            print(f"✔️ {endpoint} - Success")
        except Exception as e:
            print(f"❌ {endpoint} - Failed: {str(e)}")


if __name__ == "__main__":
    __test_endpoints()
