from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from app.database import Base

class LensInventory(Base):

    __tablename__ = "lens_inventory"

    id = Column(Integer, primary_key=True, index=True)
    lens_type = Column(String, nullable=False)
    power = Column(String, nullable=False)
    lens_index = Column(String, nullable=False)
    coating = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True)
    lens_type = Column(String)
    power = Column(String)
    lens_index = Column(String)
    coating = Column(String)
    status = Column(String, default="ORDER_PLACED")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class InventoryForecast(Base):

    __tablename__ = "inventory_forecast"

    id = Column(Integer, primary_key=True, index=True)
    lens_type = Column(String, nullable=False)
    power = Column(String, nullable=False)
    lens_index = Column(String, nullable=False)
    coating = Column(String, nullable=False)
    predicted_demand = Column(Integer)
    recommended_stock = Column(Integer)

class InventoryTransaction(Base):

    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, nullable=False)
    lens_type = Column(String, nullable=False)
    power = Column(String, nullable=False)
    lens_index = Column(String, nullable=False)
    coating = Column(String, nullable=False)
    quantity_used = Column(Integer, default=1)
    transaction_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class OrderStatusHistory(Base):

    __tablename__ = "order_status_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    old_status = Column(String)
    new_status = Column(String)
    reason = Column(String)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )