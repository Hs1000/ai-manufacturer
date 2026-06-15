from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.inventory import router as inventory_router
from app.order_service import router as order_router
from app.forecast import router as forecast_router
from app.admin import router as admin_router
from app.sla import router as sla_router
from app.dashboard import router as dashboard_router
from app.prediction import router as prediction_router
from app.alerts import router as alerts_router
from app.models import Order

Base.metadata.create_all(bind=engine)


def _auto_seed():
    """Seed data, retrain models, and generate forecasts on a fresh deploy.

    Retraining ensures .pkl files are always built with the server's
    scikit-learn version — avoids unpickling errors from version mismatches.
    """
    db = SessionLocal()
    try:
        if db.query(Order).count() == 0:
            from app.admin import seed_data
            seed_data(db)

        # Always retrain so models match the server's sklearn version
        from app.services.ml_service import build_training_dataset
        from app.ml.train_breach_model import train_model
        from app.services.forecast_ml_service import build_forecast_dataset
        from app.ml.train_forecast_model import train_forecast_model

        build_training_dataset()
        train_model()
        build_forecast_dataset()
        train_forecast_model()

        # Reload models into the prediction/forecast routers after retraining
        import importlib
        import app.prediction as pred_module
        import app.forecast as forecast_module
        import joblib

        pred_module.model = joblib.load("app/ml/breach_model.pkl")
        pred_module.lens_encoder = joblib.load("app/ml/lens_encoder.pkl")
        pred_module.status_encoder = joblib.load("app/ml/status_encoder.pkl")

        forecast_module.model = joblib.load("app/ml/forecast_model.pkl")
        forecast_module.lens_encoder = joblib.load("app/ml/forecast_lens_encoder.pkl")
        forecast_module.power_encoder = joblib.load("app/ml/forecast_power_encoder.pkl")
        forecast_module.index_encoder = joblib.load("app/ml/forecast_index_encoder.pkl")
        forecast_module.coating_encoder = joblib.load("app/ml/forecast_coating_encoder.pkl")

        # Generate forecasts with the freshly trained model
        from app.forecast import generate_forecast
        db2 = SessionLocal()
        try:
            generate_forecast(db2)
        finally:
            db2.close()

    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    _auto_seed()
    yield


app = FastAPI(
    title="AI Eyewear Order Management",
    lifespan=lifespan
)

app.include_router(inventory_router)
app.include_router(order_router)
app.include_router(forecast_router)
app.include_router(admin_router)
app.include_router(sla_router)
app.include_router(dashboard_router)
app.include_router(prediction_router)
app.include_router(alerts_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Eyewear OMS Running"
    }