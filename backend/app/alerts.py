from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    LensInventory,
    InventoryForecast,
    Order
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db)
):

    alerts = []

    # ======================
    # LOW INVENTORY
    # ======================

    inventory_items = (
        db.query(
            LensInventory
        ).all()
    )

    for item in inventory_items:

        if item.quantity < 30:

            alerts.append({

                "severity":
                    "MEDIUM",

                "type":
                    "LOW_STOCK",

                "message":
                    f"{item.lens_type} "
                    f"{item.power} "
                    f"inventory below threshold"

            })

    # ======================
    # HIGH RISK ORDERS
    # ======================

    orders = (
        db.query(
            Order
        )
        .filter(
            Order.status == "QC"
        )
        .all()
    )

    for order in orders:

        alerts.append({

            "severity":
                "HIGH",

            "type":
                "HIGH_RISK_ORDER",

            "message":
                f"{order.order_number} "
                f"requires attention"

        })

    # ======================
    # DEMAND SPIKES
    # ======================

    forecasts = (
        db.query(
            InventoryForecast
        ).all()
    )

    for forecast in forecasts:

        if (
            forecast.predicted_demand
            > 10
        ):

            alerts.append({

                "severity":
                    "INFO",

                "type":
                    "DEMAND_SPIKE",

                "message":
                    f"{forecast.lens_type} "
                    f"demand spike detected"

            })

    return alerts