from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Order,
    LensInventory,
    InventoryForecast
)


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):

    total_orders = db.query(
        Order
    ).count()

    inventory_skus = db.query(
        LensInventory
    ).count()

    forecast_records = db.query(
        InventoryForecast
    ).count()

    high_risk_orders = (
        db.query(Order)
        .filter(
            Order.status == "QC"
        )
        .count()
    )

    sla_breaches = (
        db.query(Order)
        .filter(
            Order.status == "DELIVERED"
        )
        .count()
    )

    return {

        "total_orders":
            total_orders,

        "inventory_skus":
            inventory_skus,

        "forecast_records":
            forecast_records,

        "high_risk_orders":
            high_risk_orders,

        "sla_breaches":
            sla_breaches

    }


@router.get("/order-status")
def order_status_distribution(
    db: Session = Depends(get_db)
):

    data = (
        db.query(
            Order.status,
            func.count(Order.id)
        )
        .group_by(Order.status)
        .all()
    )

    return [
        {
            "status": row[0],
            "count": row[1]
        }
        for row in data
    ]

@router.get("/forecast-demand")
def forecast_demand(
    db: Session = Depends(get_db)
):

    data = (
        db.query(
            InventoryForecast.lens_type,
            func.avg(
                InventoryForecast.predicted_demand
            )
        )
        .group_by(
            InventoryForecast.lens_type
        )
        .all()
    )

    return [
        {
            "lens_type": row[0],
            "predicted_demand": round(
                float(row[1]), 2
            )
        }
        for row in data
    ]