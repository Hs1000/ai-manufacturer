from pydantic import BaseModel

# ==========================
# Inventory Schemas
# ==========================

class InventoryCreate(BaseModel):
    lens_type: str
    power: str
    lens_index: str
    coating: str
    quantity: int


class InventoryCheck(BaseModel):
    lens_type: str
    power: str
    lens_index: str
    coating: str


# ==========================
# Order Schemas
# ==========================

class OrderCreate(BaseModel):
    order_number: str
    lens_type: str
    power: str
    lens_index: str
    coating: str


class StatusUpdate(BaseModel):
    status: str
    reason: str | None = None