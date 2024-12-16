import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from itertools import combinations
from collections import Counter


# 1. [м]
def buy_together(df: pd.DataFrame) -> pd.DataFrame:
    df_grouped = (
        df.groupby(["order_id", "customer_id"])["entity_id"].agg(list).reset_index()
    )
    df_together = df_grouped[df_grouped["entity_id"].apply(len) >= 0]
    return df_together


# 2. [м]
def popular_products_of_the_day(
    df: pd.DataFrame,
    day_date: int,      # 24
    month_date: int,    # 1 - 12
    year_date: int,     # год 2019
    flag: bool = False, # descending
) -> pd.DataFrame:
    """
    Выявление товаров на скидку в течение дня с учетом временного интервала
    """
    if day_date and month_date and year_date:
        df = df[
            (df["order_day"] == day_date)
            & (df["order_month"] == month_date)
            & (df["order_year"] == year_date)
        ]

    df = (
        df.groupby(["hour_category", "entity_id"])["hour_category"]
        .size()
        .reset_index(name="count")
    )
    df = df.sort_values(by="count", ascending=not flag)
    df = df[df["count"] >= 1]

    selected_entities: set[int] = set()
    new_df = pd.DataFrame(columns=df.columns)

    for i in range(1, 5):
        hour_group = df[
            (df["hour_category"] == i) & (~df["entity_id"].isin(selected_entities))
        ]
        if not hour_group.empty:
            median_index = hour_group.iloc[int(np.median(range(len(hour_group))))].name
            new_df.loc[len(new_df)] = df.loc[median_index]
            selected_entities.add(df.loc[median_index, "entity_id"])

    return new_df


# 3. [м]
def find_most_frequent_pairs(
    df: pd.DataFrame, customer_id: int | None = None
) -> pd.DataFrame:
    """
    Функция находит наиболее часто покупаемые вместе товары для клиента,
    если не передаём клиента -- то по общим.

    :param df: DataFrame с колонками 'order_id' и 'entity_id' [⚠️ т.е. требуется вызов buy_together] (где entity_id - список товаров)
    :return: DataFrame с парами товаров и их частотой
    """
    if customer_id is None:
        find_df = df
    else:
        find_df = df[df["customer_id"] == customer_id]

    def generate_item_pairs(item_list: list) -> list:
        return list(combinations(sorted(item_list), 2))

    all_pairs = []
    for item_list in find_df["entity_id"]:
        all_pairs.extend(generate_item_pairs(item_list))

    pair_counts = Counter(all_pairs)
    pair_counts_df = pd.DataFrame(pair_counts.items(), columns=["pair", "count"])
    pair_counts_df = pair_counts_df[
        pair_counts_df["pair"].apply(lambda x: x[0] != x[1])
    ]

    pair_counts_df_sorted = pair_counts_df.sort_values(
        by="count",
        ascending=False
    ).reset_index(drop=True)

    pair_counts_df_sorted = pair_counts_df_sorted[pair_counts_df_sorted["count"] >= 2]

    # если у клиента больше 3 пар с этим товаром
    # - мы возвращаем то что берёт обычно
    if len(pair_counts_df_sorted) < 3:
        # если недостаточно данных по парам товаров клиент
        # - мы возвращаем общее
        return find_most_frequent_pairs(df)

    return pair_counts_df_sorted

