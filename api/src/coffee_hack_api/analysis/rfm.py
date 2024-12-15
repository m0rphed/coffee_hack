import pandas as pd
from enum import StrEnum


# [в]
class RFMStatus(StrEnum):
    """
    Определяем статус клиента RFM через StrEnum
    """

    VIP = "vip"                     # "VIP статус"
    LOST = "lost"                   # Потерянный клиент"
    NEW_CUSTOMER = "new"            # "Новый клиент"
    HIGH_SPENDER = "high_spender"   # "Клиент с высоким Monetary, но редкий заказ"
    REGULAR = "regular"             # большая категория клиентов которая находится где-то "по середине"


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


# [в]
def calculate_discount(
    r: int, f: int, m: int,
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


if __name__ == "__main__":
    rfm_df = pd.DataFrame(
        {
            "customer_id": [1, 2, 3, 4, 5, 6, 7, 8],
            "RFM_score": ["555", "111", "511", "155", "455", "211", "543", "115"],
            "R_rank": [5, 1, 3, 2, 4, 5, 3, 1],
            "F_rank": [5, 1, 1, 2, 5, 3, 4, 1],
            "M_rank": [5, 1, 3, 2, 4, 3, 5, 2],
        }
    )
    # Определяем статус и скидку для каждого клиента
    rfm_df["rfm_status"] = rfm_df["RFM_score"].apply(assign_rfm_status)
    rfm_df["discount"] = rfm_df.apply(
        lambda row: calculate_discount(row["R_rank"], row["F_rank"], row["M_rank"]),
        axis=1,
    )
    print(rfm_df)