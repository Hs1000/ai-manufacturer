import pandas as pd
from datetime import datetime
from app.database import SessionLocal
from app.models import Order
from app.sla import calculate_sla


def build_dataset():

    db = SessionLocal()

    orders = db.query(Order).all()

    rows = []

    for order in orders:

        sla_info = calculate_sla(order)

        rows.append({
            "lens_type": order.lens_type,
            "status": order.status,
            "elapsed_hours": sla_info["elapsed_hours"],
            "hours_remaining": sla_info["hours_remaining"],
            "breached": int(
                sla_info["breached"]
            )
        })

    df = pd.DataFrame(rows)

    df.to_csv(
        "app/ml/training_data.csv",
        index=False
    )

    print(
        f"Dataset Created: "
        f"{len(df)} rows"
    )

    db.close()


if __name__ == "__main__":
    build_dataset()