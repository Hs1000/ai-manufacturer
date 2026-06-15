import pandas as pd
from app.database import SessionLocal
from app.models import Order
from app.sla import calculate_sla


def build_training_dataset():

    db = SessionLocal()

    orders = db.query(Order).all()

    rows = []

    for order in orders:

        sla_info = calculate_sla(order)

        rows.append({
            "lens_type": order.lens_type,
            "status": order.status,

            # Feature
            "elapsed_hours":
                sla_info["elapsed_hours"],

            # Target
            "breached":
                int(
                    sla_info["breached"]
                )
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        "app/ml/training_data.csv",
        index=False
    )

    db.close()

    return len(df)