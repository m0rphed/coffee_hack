from fastapi import FastAPI, Request
from typing import Any

app = FastAPI()


@app.post("/get_discounts")
async def get_discounts(request: Request):
    data: dict[str, Any] = await request.json()
    customer_id = data.get("customer_id")
    entity_ids = data.get("entity_ids")

    # логика вычисления скидок
    return {
        "customer_id": customer_id,
        "discounts": [
            {"entity_id": 101, "discount": 20},
            {"entity_id": 202, "discount": 15},
        ],
    }


@app.get("/customer_summary/{customer_id}")
async def get_customer_summary(customer_id: int):
    # здесь будет получение и возврат признаков клиента
    return {
        "customer_id": customer_id,
        "total_orders": 12,
        "total_items": 42,
        "avg_order_size": 3.5,
    }


@app.get("/dashboard_data")
async def get_dashboard_data():
    # данные для дашборда
    return {
        "total_customers": 1000,
        "active_customers": 200,
        "spending_trends": [120, 150, 170, 200],
    }
