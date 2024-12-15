import pandas as pd
from enum import StrEnum
import numpy as np

from coffee_hack_api.analysis.prepare import load_data


# [в]
class RFMStatus(StrEnum):
    """
    Определяем статус клиента RFM через StrEnum
    """

    VIP = "vip"  # "VIP статус"
    LOST = "lost"  # Потерянный клиент"
    NEW_CUSTOMER = "new"  # "Новый клиент"
    HIGH_SPENDER = "high_spender"  # "Клиент с высоким Monetary, но редкий заказ"
    REGULAR = (
        "regular"  # большая категория клиентов которая находится где-то "по середине"
    )


# [в]
def assign_rfm_status(rfm_score: str) -> RFMStatus:
    """
    Задаёт присвоение статуса клиента на основе RFM оценки.
    """
    match rfm_score:
        case "555":
            return RFMStatus.VIP
        case "111":
            return RFMStatus.LOST
        case "511":
            return RFMStatus.NEW_CUSTOMER
        case "155":
            return RFMStatus.HIGH_SPENDER
        case _:
            return RFMStatus.REGULAR


# [в] TODO: удостовериться в соответствии статусов с assign_rfm_status
def assign_discount(rfm_score: str) -> str:
    """
    Присваивает персональную скидку для клиента в зависимости от RFM ранга.
    """
    if rfm_score == "555":
        # Идеальные клиенты
        return "VIP статус"
    elif rfm_score == "111":
        # Потерянные клиенты
        return "Скидка 50%"
    elif rfm_score == "511":
        # Новые клиенты
        return "Скидка 20% на второй заказ"
    elif rfm_score == "155":
        # Клиенты с высоким Monetary, но редкие заказы
        return "Скидка 10% на покупку нескольких товаров"
    else:
        # Базовая скидка для всех остальных
        return "Скидка 5%"


# [в]
def calculate_discount(
    r: int,
    f: int,
    m: int,
    discount_threshold_percentage: int = 50
) -> int:
    """
    Рассчитывает скидку для клиента на основе рангов R, F и M.
    """
    # [эвристика] чем меньше R, тем больше скидка
    recency_discount = (6 - r) * 2
    # [эвристика] чем меньше F, тем больше скидка
    frequency_discount = (6 - f) * 2
    # [эвристика] чем меньше M, тем больше скидка
    monetary_discount = 6 - m
    total_discount = recency_discount + frequency_discount + monetary_discount
    # ограничиваем максимум до 50%
    return min(total_discount, discount_threshold_percentage)


def prepare_rfm(df: pd.DataFrame, intervals_count: int = 5):
    def _get_intervals_labels(intervals_n: int) -> list:
        return list(range(1, intervals_n + 1))

    # Текущая дата анализа (например, максимальная дата из данных)
    current_date = df["create_datetime"].max()

    # дата последней покупки для каждого клиента
    recency_df = df.groupby("customer_id")["create_datetime"].max().reset_index()

    # дней с последнего захода
    recency_df["days_since_last_purchase"] = (
        current_date - recency_df["create_datetime"]
    ).dt.days

    monetary_df = df.groupby("customer_id")["entity_id"].count().reset_index()
    monetary_df.rename(columns={"entity_id": "total_items"}, inplace=True)

    # количество (разных) заказов в кофейнях для каждого гостя
    frequency_df = df.groupby("customer_id")["order_id"].nunique().reset_index()
    frequency_df.rename(columns={"order_id": "order_count"}, inplace=True)

    # среднее количество позиций в заказах для клиента
    average_items_df = (
        df.groupby(["customer_id", "order_id"])["entity_id"].count().reset_index()
    )
    average_items_df = (
        average_items_df.groupby("customer_id")["entity_id"].mean().reset_index()
    )
    average_items_df.rename(columns={"entity_id": "avg_items_per_order"}, inplace=True)
    # сколько в среднем покупает клиент за 1 заказ

    # объединяем метрики в единый DataFrame
    rfm_df = (
        recency_df[["customer_id", "days_since_last_purchase"]]
        .merge(
            frequency_df[["customer_id", "order_count"]],
            on="customer_id",
            how="left"
        )
        .merge(
            monetary_df[["customer_id", "total_items"]],
            on="customer_id",
            how="left"
        )
        .merge(
            average_items_df[["customer_id", "avg_items_per_order"]],
            on="customer_id",
            how="left",
        )
    )

    # Разделяем метрики на квантильные категории
    rfm_df["R_rank"] = pd.qcut(
        rfm_df["days_since_last_purchase"],
        intervals_count,
        labels=_get_intervals_labels(intervals_count),
    )

    # Добавляем небольшой шум к order_count
    rfm_df["order_count_noisy"] = rfm_df["order_count"] + np.random.normal(
        0, 1e-5, size=len(rfm_df)
    )

    # Применяем pd.qcut с шумом
    rfm_df["F_rank"] = pd.qcut(
        rfm_df["order_count_noisy"],
        intervals_count,
        labels=_get_intervals_labels(intervals_count),
    )

    # Добавляем небольшой шум к total_items
    rfm_df["total_items_noisy"] = rfm_df["total_items"] + np.random.normal(
        0, 1e-5, size=len(rfm_df)
    )
    rfm_df["M_rank"] = pd.qcut(
        rfm_df["total_items_noisy"],
        intervals_count,
        labels=_get_intervals_labels(intervals_count),
    )

    rfm_df["RFM_score"] = (
        rfm_df["R_rank"].astype(str)
        + rfm_df["F_rank"].astype(str)
        + rfm_df["M_rank"].astype(str)
    )

    return rfm_df


# [в] [not_ready]
def calculate_combined_discount(row):
    """
    Рассчитывает скидку для клиента с учетом сегмента RFM и динамической системы скидок.
    """
    r, f, m, rfm_score = (
        row["R_rank"],
        row["F_rank"],
        row["M_rank"],
        row["RFM_score"]
    )

    # персонализация по RFM сегменту
    segment_discount = assign_discount(rfm_score)

    # динамическая скидка на основе рангов R, F, M
    dynamic_discount = calculate_discount(r, f, m)

    # применяем итоговую скидку
    return segment_discount if "Скидка" in segment_discount else f"{dynamic_discount}%"


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    # загружаем .env файл с указанием пути к .csv
    load_dotenv()

    file_path = os.environ.get("DATASET_CSV_FILE")
    if file_path is None:
        raise RuntimeError(f"Ошибка загрузки датасета из .csv: '{file_path}'")

    df: pd.DataFrame = load_data(file_path)
    rfm_df = prepare_rfm(df)
    
    # определяем статус и скидку для каждого клиента
    rfm_df["rfm_status"] = rfm_df["RFM_score"].apply(assign_rfm_status)
    rfm_df["discount"] = rfm_df.apply(
        lambda row: calculate_discount(
            row["R_rank"],
            row["F_rank"],
            row["M_rank"]
        ),
        axis=1,
    )
    print(rfm_df)
