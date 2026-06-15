import pandas as pd
from app.database import SessionLocal
from app.models import InventoryTransaction


def build_forecast_dataset():

    db = SessionLocal()

    transactions = (
        db.query(
            InventoryTransaction
        ).all()
    )

    rows = []

    for tx in transactions:

        rows.append({

            "lens_type":
                tx.lens_type,

            "power":
                tx.power,

            "lens_index":
                tx.lens_index,

            "coating":
                tx.coating,

            "quantity_used":
                tx.quantity_used

        })

    df = pd.DataFrame(rows)

    df.to_csv(
        "app/ml/forecast_training.csv",
        index=False
    )

    db.close()

    return len(df)