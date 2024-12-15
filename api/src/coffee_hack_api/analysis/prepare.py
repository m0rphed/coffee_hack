import pandas as pd

# [м]
def preprocess_data(df: pd.DataFrame):
    # сезоны года
    # seasons = {
    #     "winter": [1, 2, 12],
    #     "spring": [3, 4, 5],
    #     "summer": [6, 7, 8],
    #     "autumn": [9, 10, 11],
    # }
    
    # часы работы 
    hours = {
        1: [6,7,8,9,10],
        2: [11,12,13,14,15],
        3: [16,17,18,19,20],
        4: [21,22,23,0,1]
    }
    
    # df["create_datetime"] = pd.to_datetime(df["create_datetime"])
    df["order_day"] = df["create_datetime"].dt.day
    df["order_hour"] = df["create_datetime"].dt.hour
    df["order_weekday"] = df["create_datetime"].dt.weekday
    df["order_month"] = df["create_datetime"].dt.month
    df["order_year"] = df["create_datetime"].dt.year
    df["day_of_week_name"] = df["create_datetime"].dt.day_name()
    df["order_week"] = df["create_datetime"].dt.isocalendar().week

    def categorize_hour(hour):
        for category, hour_list in hours.items():
            if hour in hour_list:
                return category
        # на случай, если час не попадает в список
        return None
    # TODO: возможно в данных будет None, но на данный момент таких значений нет 
    # "hour_category" - категория по времени
    df["hour_category"] = df["order_hour"].apply(categorize_hour)
    return df

# [м]
def load_data(file_path: str) -> pd.DataFrame:
    """
    Загрузка и очистка (дубликаты) данных
    """
    df = pd.read_csv(
        file_path,
        sep=";",
        quotechar='"'
    )
    df["create_datetime"] = pd.to_datetime(df["create_datetime"])
    df = df.drop_duplicates(subset=["id"])
    df = df.dropna(subset=["entity_id"])
    return df

if __name__ == "":
    pass