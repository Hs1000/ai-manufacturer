import joblib

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models import (
    InventoryForecast,
    InventoryTransaction
)

router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load(
    "app/ml/forecast_model.pkl"
)

lens_encoder = joblib.load(
    "app/ml/forecast_lens_encoder.pkl"
)

power_encoder = joblib.load(
    "app/ml/forecast_power_encoder.pkl"
)

index_encoder = joblib.load(
    "app/ml/forecast_index_encoder.pkl"
)

coating_encoder = joblib.load(
    "app/ml/forecast_coating_encoder.pkl"
)


@router.get("/")
def get_forecasts(
    db: Session = Depends(get_db)
):

    return db.query(
        InventoryForecast
    ).all()


@router.post("/generate")
def generate_forecast(
    db: Session = Depends(get_db)
):

    db.query(
        InventoryForecast
    ).delete()

    db.commit()

    demand_data = (
        db.query(
            InventoryTransaction.lens_type,
            InventoryTransaction.power,
            InventoryTransaction.lens_index,
            InventoryTransaction.coating
        )
        .distinct()
        .all()
    )

    forecasts = []

    for row in demand_data:

        features = [[

            lens_encoder.transform(
                [row.lens_type]
            )[0],

            power_encoder.transform(
                [row.power]
            )[0],

            index_encoder.transform(
                [row.lens_index]
            )[0],

            coating_encoder.transform(
                [row.coating]
            )[0]

        ]]

        predicted_demand = float(
            model.predict(
                features
            )[0]
        )

        recommended_stock = int(
            predicted_demand * 1.30
        )

        forecast = InventoryForecast(

            lens_type=row.lens_type,

            power=row.power,

            lens_index=row.lens_index,

            coating=row.coating,

            predicted_demand=round(
                predicted_demand,
                2
            ),

            recommended_stock=
                recommended_stock

        )

        db.add(
            forecast
        )

        forecasts.append({

            "lens_type":
                row.lens_type,

            "power":
                row.power,

            "predicted_demand":
                round(
                    predicted_demand,
                    2
                ),

            "recommended_stock":
                recommended_stock

        })

    db.commit()

    return forecasts