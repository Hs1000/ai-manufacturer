from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.inventory import router as inventory_router
from app.order_service import router as order_router
from app.forecast import router as forecast_router
from app.admin import router as admin_router
from app.sla import router as sla_router
from app.dashboard import router as dashboard_router
from app.prediction import router as prediction_router
from app.alerts import router as alerts_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Eyewear Order Management"
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