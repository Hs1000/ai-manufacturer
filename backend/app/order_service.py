from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    Order,
    LensInventory,
    InventoryTransaction,
    OrderStatusHistory
)

from app.schemas import (
    OrderCreate,
    StatusUpdate
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# =====================================
# Create Order
# =====================================

@router.post("/")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    inventory = (
        db.query(LensInventory)
        .filter(
            LensInventory.lens_type == order.lens_type,
            LensInventory.power == order.power,
            LensInventory.lens_index == order.lens_index,
            LensInventory.coating == order.coating
        )
        .first()
    )

    if not inventory:

        status = "OUT_OF_STOCK"

    elif inventory.quantity <= 0:

        status = "OUT_OF_STOCK"

    else:

        inventory.quantity -= 1
        status = "ORDER_PLACED"

        transaction = InventoryTransaction(
            order_number=order.order_number,
            lens_type=order.lens_type,
            power=order.power,
            lens_index=order.lens_index,
            coating=order.coating,
            quantity_used=1
        )

        db.add(transaction)

    new_order = Order(
        order_number=order.order_number,
        lens_type=order.lens_type,
        power=order.power,
        lens_index=order.lens_index,
        coating=order.coating,
        status=status
    )

    db.add(new_order)

    db.flush()

    history = OrderStatusHistory(
        order_id=new_order.id,
        old_status=None,
        new_status=status,
        reason="Order Created"
    )

    db.add(history)

    db.commit()
    db.refresh(new_order)

    return {
        "order_id": new_order.id,
        "order_number": new_order.order_number,
        "status": status
    }


# =====================================
# Update Order Status
# =====================================

@router.post("/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    old_status = order.status

    order.status = payload.status

    history = OrderStatusHistory(
        order_id=order.id,
        old_status=old_status,
        new_status=payload.status,
        reason=payload.reason
    )

    db.add(history)

    db.commit()

    return {
        "message": "Status updated",
        "order_id": order.id,
        "old_status": old_status,
        "new_status": payload.status
    }


# =====================================
# Get Order Timeline
# =====================================

@router.get("/{order_id}/timeline")
def get_order_timeline(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    timeline = (
        db.query(OrderStatusHistory)
        .filter(
            OrderStatusHistory.order_id == order_id
        )
        .order_by(
            OrderStatusHistory.updated_at
        )
        .all()
    )

    return timeline


# =====================================
# Get All Orders
# =====================================

@router.get("/")
def get_orders(
    db: Session = Depends(get_db)
):

    return db.query(Order).all()