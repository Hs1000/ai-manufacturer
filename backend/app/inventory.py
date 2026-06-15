from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import LensInventory
from app.schemas import InventoryCreate, InventoryCheck
from app.models import (
    LensInventory,
    InventoryForecast
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post("/")
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):

    item = LensInventory(
        lens_type=inventory.lens_type,
        power=inventory.power,
        lens_index=inventory.lens_index,
        coating=inventory.coating,
        quantity=inventory.quantity
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("/")
def get_inventory(
    db: Session = Depends(get_db)
):

    return db.query(LensInventory).all()


@router.post("/check")
def check_inventory(
    payload: InventoryCheck,
    db: Session = Depends(get_db)
):

    item = (
        db.query(LensInventory)
        .filter(
            LensInventory.lens_type == payload.lens_type,
            LensInventory.power == payload.power,
            LensInventory.lens_index == payload.lens_index,
            LensInventory.coating == payload.coating
        )
        .first()
    )

    if not item:
        return {
            "available": False,
            "message": "Lens not found"
        }

    return {
        "available": item.quantity > 0,
        "quantity": item.quantity
    }


@router.get("/health")
def inventory_health(
    db: Session = Depends(get_db)
):

    inventory_items = db.query(
        LensInventory
    ).all()

    response = []

    for item in inventory_items:

        forecast = (
            db.query(InventoryForecast)
            .filter(
                InventoryForecast.lens_type == item.lens_type,
                InventoryForecast.power == item.power,
                InventoryForecast.lens_index == item.lens_index,
                InventoryForecast.coating == item.coating
            )
            .first()
        )

        if not forecast:
            continue

        current_stock = item.quantity

        recommended_stock = (
            forecast.recommended_stock
        )

        shortage = max(
            0,
            recommended_stock - current_stock
        )

        if current_stock < recommended_stock:
            status = "LOW_STOCK"

        elif current_stock < (
            recommended_stock * 1.2
        ):
            status = "WARNING"

        else:
            status = "HEALTHY"

        response.append({
            "lens_type": item.lens_type,
            "power": item.power,
            "lens_index": item.lens_index,
            "coating": item.coating,
            "current_stock": current_stock,
            "recommended_stock": recommended_stock,
            "shortage": shortage,
            "status": status
        })

    return response