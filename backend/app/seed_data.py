import random
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import (
    LensInventory,
    Order,
    InventoryTransaction
)

db = SessionLocal()

# -----------------------------
# Sample Data
# -----------------------------

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

# -----------------------------
# Seed Inventory
# -----------------------------

print("Creating Inventory...")

for lens_type in lens_types:
    for power in powers:
        for index in indices:
            for coating in coatings:

                inventory = LensInventory(
                    lens_type=lens_type,
                    power=power,
                    lens_index=index,
                    coating=coating,
                    quantity=random.randint(20, 100)
                )

                db.add(inventory)

db.commit()

print("Inventory Created")


# -----------------------------
# Seed Orders + Transactions
# -----------------------------

print("Creating Orders & Transactions...")

for i in range(500):

    lens_type = random.choice(lens_types)
    power = random.choice(powers)
    index = random.choice(indices)
    coating = random.choice(coatings)

    order_number = f"ORD{i+1:05d}"

    created_date = (
        datetime.now()
        - timedelta(days=random.randint(1, 180))
    )

    order = Order(
        order_number=order_number,
        lens_type=lens_type,
        power=power,
        lens_index=index,
        coating=coating,
        status="DELIVERED"
    )

    db.add(order)

    transaction = InventoryTransaction(
        order_number=order_number,
        lens_type=lens_type,
        power=power,
        lens_index=index,
        coating=coating,
        quantity_used=1,
        transaction_date=created_date
    )

    db.add(transaction)

db.commit()

print("Orders Created")
print("Transactions Created")

db.close()

print("Seeding Complete")