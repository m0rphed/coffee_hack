import pandas as pd

# import numpy as np
from typing import Callable
from coffee_hack_api.analysis.prepare import load_data


# 1.
def calculate_total_orders(data: pd.DataFrame) -> pd.DataFrame:
    """
    Количество заказов (число уникальных order_id)
    """
    customer_orders = data.groupby("customer_id")["order_id"].nunique().reset_index()
    customer_orders.rename(columns={"order_id": "total_orders"}, inplace=True)
    return customer_orders


# 2.
def calculate_total_items(data: pd.DataFrame) -> pd.DataFrame:
    """
    Общее количество купленных товаров (количество entity_id для клиента)
    """
    customer_total_items = (
        data.groupby("customer_id")["entity_id"].count().reset_index()
    )
    customer_total_items.rename(columns={"entity_id": "total_items"}, inplace=True)
    return customer_total_items


# 3.
def calculate_avg_order_size(data: pd.DataFrame) -> pd.DataFrame:
    """
    Средний размер заказа (количество товаров на один order_id)
    """
    customer_order_sizes = (
        data.groupby(["customer_id", "order_id"])["entity_id"].count().reset_index()
    )
    customer_avg_order_size = (
        customer_order_sizes.groupby("customer_id")["entity_id"].mean().reset_index()
    )
    customer_avg_order_size.rename(
        columns={"entity_id": "avg_order_size"}, inplace=True
    )
    return customer_avg_order_size


# 4.
def calculate_avg_order_interval(data: pd.DataFrame) -> pd.DataFrame:
    """
    Частота заказов (интервал между заказами)
    """
    customer_order_times = (
        data.groupby(["customer_id", "order_id"])["create_datetime"].min().reset_index()
    )
    customer_order_times["prev_order_time"] = customer_order_times.groupby(
        "customer_id"
    )["create_datetime"].shift(1)

    customer_order_times["order_interval"] = (
        customer_order_times["create_datetime"]
        - customer_order_times["prev_order_time"]
    ).dt.total_seconds() / 3600  # интервал будет в часах

    customer_avg_order_interval = (
        customer_order_times.groupby("customer_id")["order_interval"]
        .mean()
        .reset_index()
    )

    customer_avg_order_interval.rename(
        columns={"order_interval": "avg_order_interval_hours"}, inplace=True
    )
    return customer_avg_order_interval


# 5.
def calculate_unique_items(data: pd.DataFrame) -> pd.DataFrame:
    """
    Количество уникальных товаров, которые клиент купил
    """
    customer_unique_items = (
        data.groupby("customer_id")["entity_id"].nunique().reset_index()
    )
    customer_unique_items.rename(columns={"entity_id": "unique_items"}, inplace=True)
    return customer_unique_items


# === объединяем все признаки в единую таблицу ===
def combine_customer_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Объединение всех признаков в одну таблицу.
    """
    feature_functions: list[Callable[[pd.DataFrame], pd.DataFrame]] = [
        calculate_total_orders,
        calculate_total_items,
        calculate_avg_order_size,
        calculate_avg_order_interval,
        calculate_unique_items,
    ]

    customer_features: pd.DataFrame | None = None
    for func in feature_functions:
        feature_df = func(data)
        if customer_features is None:
            customer_features = feature_df
        else:
            customer_features = customer_features.merge(
                feature_df, on="customer_id", how="left"
            )

    if customer_features is None:
        raise RuntimeError(
            f"Ошибка преобразования данных 'customer_features' is {customer_features}"
        )

    # заполним возможные пропуски (NaN) нулями, если они появились (TODO: проверить)
    customer_features.fillna(0, inplace=True)
    return customer_features


DATAFRAME_CACHE: pd.DataFrame = None


# главная функция для загрузки данных и генерации признаков клиента
def _prepare_customer_features(file_path: str) -> pd.DataFrame:
    global DATAFRAME_CACHE
    if DATAFRAME_CACHE is None:
        DATAFRAME_CACHE = load_data(file_path)
    customer_features = combine_customer_features(DATAFRAME_CACHE)
    print(customer_features)
    return customer_features


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    # загружаем .env файл с указанием пути к .csv
    load_dotenv()

    file_path = os.environ.get("DATASET_CSV_FILE")
    if file_path is None:
        raise RuntimeError(f"Ошибка загрузки датасета из .csv: '{file_path}'")

    _df_customer_features: pd.DataFrame = _prepare_customer_features(file_path)
    print(_df_customer_features.head(10))
    print(_df_customer_features.nunique())
