import joblib

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Order
from app.sla import calculate_sla

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)

# ==========================
# LOAD MODEL
# ==========================

model = joblib.load(
    "app/ml/breach_model.pkl"
)

lens_encoder = joblib.load(
    "app/ml/lens_encoder.pkl"
)

status_encoder = joblib.load(
    "app/ml/status_encoder.pkl"
)


# ==========================
# HELPERS
# ==========================

def get_risk_level(probability):

    if probability >= 0.80:
        return "HIGH"

    elif probability >= 0.40:
        return "MEDIUM"

    return "LOW"


def prepare_features(order):

    sla_info = calculate_sla(order)

    lens_type = lens_encoder.transform(
        [order.lens_type]
    )[0]

    status = status_encoder.transform(
        [order.status]
    )[0]

    elapsed_hours = sla_info[
        "elapsed_hours"
    ]

    return [[
        lens_type,
        status,
        elapsed_hours
    ]]


def predict_probability(order):

    features = prepare_features(
        order
    )

    probability = (
        model.predict_proba(
            features
        )[0][1]
    )

    return round(
        float(probability),
        2
    )


# ==========================
# ALL PREDICTIONS
# ==========================

@router.get("/orders")
def prediction_orders(
    db: Session = Depends(get_db)
):

    orders = db.query(
        Order
    ).all()

    results = []

    for order in orders:

        probability = (
            predict_probability(
                order
            )
        )

        results.append({

            "order_id":
                order.id,

            "order_number":
                order.order_number,

            "lens_type":
                order.lens_type,

            "status":
                order.status,

            "breach_probability":
                probability,

            "risk_level":
                get_risk_level(
                    probability
                )

        })

    results.sort(
        key=lambda x:
        x["breach_probability"],
        reverse=True
    )

    return results


# ==========================
# SUMMARY CARDS
# ==========================

@router.get("/summary")
def prediction_summary(
    db: Session = Depends(get_db)
):

    orders = db.query(
        Order
    ).all()

    high = 0
    medium = 0
    low = 0

    for order in orders:

        probability = (
            predict_probability(
                order
            )
        )

        risk = get_risk_level(
            probability
        )

        if risk == "HIGH":
            high += 1

        elif risk == "MEDIUM":
            medium += 1

        else:
            low += 1

    return {
        "high": high,
        "medium": medium,
        "low": low
    }


# ==========================
# HIGH RISK ONLY
# ==========================

@router.get("/high-risk")
def high_risk_orders(
    db: Session = Depends(get_db)
):

    orders = db.query(
        Order
    ).all()

    results = []

    for order in orders:

        probability = (
            predict_probability(
                order
            )
        )

        if probability >= 0.80:

            results.append({

                "order_id":
                    order.id,

                "order_number":
                    order.order_number,

                "lens_type":
                    order.lens_type,

                "status":
                    order.status,

                "breach_probability":
                    probability,

                "risk_level":
                    "HIGH"

            })

    return results