from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order

router = APIRouter(
    prefix="/sla",
    tags=["SLA"]
)

# SLA in Hours
SLA_RULES = {
    "Single Vision": 48,
    "Progressive": 120,
    "Blue Light": 72
}


def get_sla_hours(lens_type: str):

    return SLA_RULES.get(
        lens_type,
        72
    )


def calculate_sla(order):

    sla_hours = get_sla_hours(
        order.lens_type
    )

    created_at = order.created_at

    elapsed_hours = (
        datetime.utcnow() - created_at
    ).total_seconds() / 3600

    hours_remaining = (
        sla_hours - elapsed_hours
    )

    breached = (
        hours_remaining < 0
    )

    return {
        "sla_hours": round(sla_hours, 2),
        "elapsed_hours": round(elapsed_hours, 2),
        "hours_remaining": round(hours_remaining, 2),
        "breached": breached
    }


@router.get("/orders")
def get_order_sla_dashboard(
    status: str = None,
    lens_type: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Order)

    if status:
        query = query.filter(Order.status == status)

    if lens_type:
        query = query.filter(Order.lens_type == lens_type)

    orders = query.all()

    response = []

    for order in orders:

        sla_info = calculate_sla(
            order
        )

        response.append({
            "order_id": order.id,
            "order_number": order.order_number,
            "lens_type": order.lens_type,
            "status": order.status,
            "sla_hours": sla_info["sla_hours"],
            "elapsed_hours": sla_info["elapsed_hours"],
            "hours_remaining": sla_info["hours_remaining"],
            "breached": sla_info["breached"]
        })

    return response