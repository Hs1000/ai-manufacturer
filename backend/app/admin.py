from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from datetime import datetime
from datetime import timedelta

import random

from app.database import get_db

from app.models import (
    Order,
    LensInventory,
    InventoryTransaction
)

from app.services.ml_service import (
    build_training_dataset
)

from app.ml.train_breach_model import (
    train_model
)

from app.services.forecast_ml_service import (
    build_forecast_dataset
)

from app.ml.train_forecast_model import (
    train_forecast_model
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/seed-data")
def seed_data(
    db: Session = Depends(get_db)
):

    # ==========================================
    # CLEAR OLD DATA
    # ==========================================

    db.query(
        InventoryTransaction
    ).delete()

    db.query(
        Order
    ).delete()

    db.query(
        LensInventory
    ).delete()

    db.commit()

    # ==========================================
    # MASTER DATA
    # ==========================================

    lens_types = [
        "Single Vision",
        "Progressive",
        "Blue Light"
    ]

    powers = [
        "-1.00",
        "-1.50",
        "-2.00",
        "-2.25",
        "-2.50",
        "-3.00"
    ]

    indices = [
        "1.50",
        "1.60",
        "1.67"
    ]

    coatings = [
        "Anti Glare",
        "Blue Light",
        "UV Protection"
    ]

    statuses = [
        "ORDER_PLACED",
        "PRESCRIPTION_VALIDATED",
        "LENS_CUTTING",
        "COATING",
        "ASSEMBLY",
        "QC",
        "DISPATCHED",
        "DELIVERED"
    ]

    inventory_count = 0
    order_count = 0

    # ==========================================
    # INVENTORY
    # ==========================================

    for lens_type in lens_types:

        for power in powers:

            for index in indices:

                for coating in coatings:

                    if lens_type == "Single Vision":

                        stock_qty = random.randint(
                            80,
                            150
                        )

                    elif lens_type == "Blue Light":

                        stock_qty = random.randint(
                            40,
                            100
                        )

                    else:

                        stock_qty = random.randint(
                            20,
                            60
                        )

                    inventory = LensInventory(
                        lens_type=lens_type,
                        power=power,
                        lens_index=index,
                        coating=coating,
                        quantity=stock_qty
                    )

                    db.add(
                        inventory
                    )

                    inventory_count += 1

    db.commit()

    # ==========================================
    # ORDERS + TRANSACTIONS
    # ==========================================

    for i in range(500):

        lens_type = random.choice(
            lens_types
        )

        power = random.choice(
            powers
        )

        index = random.choice(
            indices
        )

        coating = random.choice(
            coatings
        )

        status = random.choice(
            statuses
        )

        order_number = (
            f"ORD{i+1:05d}"
        )

        created_date = (
            datetime.utcnow()
            - timedelta(
                hours=random.randint(
                    1,
                    120
                )
            )
        )

        order = Order(
            order_number=order_number,
            lens_type=lens_type,
            power=power,
            lens_index=index,
            coating=coating,
            status=status,
            created_at=created_date
        )

        db.add(order)

        if lens_type == "Single Vision":

            quantity_used = (
                random.randint(
                    5,
                    15
                )
            )

        elif lens_type == "Blue Light":

            quantity_used = (
                random.randint(
                    3,
                    10
                )
            )

        else:

            quantity_used = (
                random.randint(
                    1,
                    6
                )
            )

        transaction = (
            InventoryTransaction(
                order_number=order_number,
                lens_type=lens_type,
                power=power,
                lens_index=index,
                coating=coating,
                quantity_used=quantity_used,
                transaction_date=created_date
            )
        )

        db.add(
            transaction
        )

        order_count += 1

    db.commit()

    return {

        "message":
            "Demo data generated successfully",

        "inventory_records":
            inventory_count,

        "orders_created":
            order_count,

        "transactions_created":
            order_count

    }


@router.post("/train-model")
def train_breach_prediction_model():

    dataset_rows = (
        build_training_dataset()
    )

    model_info = (
        train_model()
    )

    return {

        "message":
            "Breach prediction model trained",

        "dataset_rows":
            dataset_rows,

        "trained_rows":
            model_info["rows"]

    }


@router.post("/train-forecast-model")
def train_inventory_forecast_model():

    dataset_rows = (
        build_forecast_dataset()
    )

    trained_rows = (
        train_forecast_model()
    )

    return {

        "message":
            "Forecast model trained",

        "dataset_rows":
            dataset_rows,

        "trained_rows":
            trained_rows

    }