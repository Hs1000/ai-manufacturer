# AI-Powered Eyewear Order Management System

## Live Deployment

| Layer    | URL                                        |
| -------- | ------------------------------------------ |
| Frontend | Vercel (see Vercel dashboard after deploy) |
| Backend  | https://ai-manufacturer.onrender.com       |
| API Docs | https://ai-manufacturer.onrender.com/docs  |

---

## Overview

The AI-Powered Eyewear Order Management System is a full-stack application designed to manage eyewear manufacturing operations, inventory planning, order lifecycle tracking, SLA monitoring, and predictive analytics.

The platform combines operational dashboards with machine learning models to help manufacturing teams proactively manage inventory demand and identify orders at risk of breaching service-level agreements (SLAs).

---

## Prerequisites

| Requirement | Version |
| ----------- | ------- |
| Python      | 3.9+    |
| Node.js     | 18+     |
| npm         | 9+      |

---

## Project Structure

```
ai-manufacturer/
├── requirements.txt                  # Backend Python dependencies (install from root)
├── backend/
│   └── app/
│       ├── main.py                   # FastAPI app + router registration
│       ├── models.py                 # SQLAlchemy ORM models
│       ├── schemas.py                # Pydantic request/response schemas
│       ├── database.py               # SQLite engine + session factory
│       ├── admin.py                  # Seed data + model training endpoints
│       ├── order_service.py          # Order CRUD + status transitions
│       ├── inventory.py              # Inventory management
│       ├── sla.py                    # SLA calculation + monitoring
│       ├── prediction.py             # Breach probability inference
│       ├── forecast.py               # Demand forecast inference
│       ├── dashboard.py              # KPI summary endpoints
│       ├── alerts.py                 # Alert generation
│       └── ml/
│           ├── train_breach_model.py      # Trains breach classifier
│           ├── train_forecast_model.py    # Trains demand regressor
│           ├── breach_model.pkl           # Trained RandomForestClassifier
│           ├── forecast_model.pkl         # Trained RandomForestRegressor
│           ├── lens_encoder.pkl           # LabelEncoder for lens type (breach model)
│           ├── status_encoder.pkl         # LabelEncoder for order status
│           ├── forecast_*_encoder.pkl     # Encoders for forecast features
│           └── training_data.csv          # Training dataset (breach model)
└── frontend/
    ├── package.json
    └── src/
        ├── App.jsx                   # Routes
        ├── api/api.js                # Axios base config (http://localhost:8000)
        ├── components/               # Navbar, SummaryCards, DataTable, DashboardContainer
        └── pages/
            ├── HomeDashboard.jsx
            ├── OrderDashboard.jsx
            ├── InventoryDashboard.jsx
            ├── ForecastDashboard.jsx
            ├── PredictionDashboard.jsx
            └── AlertsDashboard.jsx
```

---

## Key Features

### Inventory Management

* Manage lens inventory across different lens types, powers, indices, and coatings.
* Monitor inventory availability and stock levels.
* Track inventory consumption through transactions.

### Order Lifecycle Management

* Create and manage customer orders.
* Track manufacturing progress through production stages.
* Monitor order status throughout the fulfillment lifecycle.

### SLA Monitoring

* Define SLA targets based on lens type.
* Calculate elapsed processing time.
* Detect SLA breaches in real-time.

### AI Demand Forecasting

* Uses a Random Forest Regressor to predict expected inventory demand.
* Generates stock recommendations based on predicted demand (predicted demand × 1.30 buffer).
* Helps operations teams optimize inventory planning.

### AI SLA Breach Prediction

* Uses a Random Forest Classifier to estimate the probability of SLA breaches.
* Categorizes orders into:

  * High Risk (≥ 80%)
  * Medium Risk (40–79%)
  * Low Risk (< 40%)
* Enables proactive operational intervention.

### Executive Dashboard

* KPI overview for operational health.
* Forecast insights.
* Risk monitoring.
* Inventory visibility.

### Alert Center

* Low inventory alerts (quantity < 30 units).
* High-risk order alerts (orders currently in QC status).
* Demand spike alerts (predicted demand > 10 units).

---

## System Architecture

Frontend:

* React 19
* React Router 7
* Axios
* Material UI
* Recharts

Backend:

* FastAPI
* SQLAlchemy
* SQLite (`backend/eyewear.db`, auto-created on first run)

Machine Learning:

* Scikit-learn
* Random Forest Classifier (breach prediction)
* Random Forest Regressor (demand forecast)
* Pandas
* Joblib

---

## SLA Rules

SLA targets are defined per lens type. The breach classifier is trained against these thresholds.

| Lens Type     | SLA Target |
| ------------- | ---------- |
| Single Vision | 48 hours   |
| Progressive   | 120 hours  |
| Blue Light    | 72 hours   |

Orders that exceed their SLA target are marked `breached = True` and become candidates for HIGH risk classification.

---

## Order Status Lifecycle

Orders move through the following stages in sequence:

```
ORDER_PLACED → PRESCRIPTION_VALIDATED → LENS_CUTTING → COATING → ASSEMBLY → QC → DISPATCHED → DELIVERED
```

| Status                 | Description                         |
| ---------------------- | ----------------------------------- |
| ORDER_PLACED           | Order received, inventory reserved  |
| PRESCRIPTION_VALIDATED | Prescription check passed           |
| LENS_CUTTING           | Lens cutting in progress            |
| COATING                | Coating applied                     |
| ASSEMBLY               | Lens assembled into frame           |
| QC                     | Quality control inspection          |
| DISPATCHED             | Shipped to customer                 |
| DELIVERED              | Order fulfilled                     |

If inventory is unavailable at order creation, status is set to `OUT_OF_STOCK` and no inventory is deducted.

---

## Database Schema

### Orders

| Column       | Description                 |
| ------------ | --------------------------- |
| id           | Primary Key                 |
| order_number | Unique Order ID             |
| lens_type    | Lens Category               |
| power        | Lens Power                  |
| lens_index   | Lens Index                  |
| coating      | Lens Coating                |
| status       | Current Manufacturing Stage |
| created_at   | Order Creation Time         |

### LensInventory

| Column     | Description         |
| ---------- | ------------------- |
| id         | Primary Key         |
| lens_type  | Lens Category       |
| power      | Lens Power          |
| lens_index | Lens Index          |
| coating    | Lens Coating        |
| quantity   | Available Inventory |

### InventoryTransaction

| Column           | Description          |
| ---------------- | -------------------- |
| id               | Primary Key          |
| order_number     | Associated Order     |
| lens_type        | Lens Category        |
| power            | Lens Power           |
| lens_index       | Lens Index           |
| coating          | Lens Coating         |
| quantity_used    | Consumption Quantity |
| transaction_date | Consumption Date     |

### InventoryForecast

| Column            | Description               |
| ----------------- | ------------------------- |
| id                | Primary Key               |
| lens_type         | Lens Category             |
| power             | Lens Power                |
| lens_index        | Lens Index                |
| coating           | Lens Coating              |
| predicted_demand  | ML Predicted Demand       |
| recommended_stock | Suggested Inventory Level |

### OrderStatusHistory

| Column     | Description              |
| ---------- | ------------------------ |
| id         | Primary Key              |
| order_id   | Associated Order         |
| old_status | Previous Status          |
| new_status | Updated Status           |
| reason     | Reason for status change |
| updated_at | Timestamp of change      |

---

## Machine Learning Components

### SLA Breach Prediction

Model: `RandomForestClassifier(n_estimators=100, random_state=42)`

| Feature       | Importance |
| ------------- | ---------- |
| elapsed_hours | 59.4%      |
| lens_type     | 37.9%      |
| status        | 2.7%       |

Target: `breached` (1 = SLA exceeded, 0 = within SLA)

Output: `breach_probability` (0.0–1.0) and `risk_level` (HIGH / MEDIUM / LOW)

Artifacts: `app/ml/breach_model.pkl`, `lens_encoder.pkl`, `status_encoder.pkl`

---

### Inventory Demand Forecasting

Model: `RandomForestRegressor`

Features: Lens Type, Power, Lens Index, Coating

Target: Quantity Used (from `InventoryTransaction`)

Output: `predicted_demand` and `recommended_stock` (predicted × 1.30)

Artifacts: `app/ml/forecast_model.pkl`, `forecast_lens_encoder.pkl`, `forecast_power_encoder.pkl`, `forecast_index_encoder.pkl`, `forecast_coating_encoder.pkl`

---

## API Endpoints

### Inventory

| Method | Path                 | Description                        |
| ------ | -------------------- | ---------------------------------- |
| GET    | /inventory/          | List all inventory SKUs            |
| POST   | /inventory/          | Add a new inventory SKU            |
| POST   | /inventory/check     | Check availability for a SKU       |
| GET    | /inventory/health    | Stock health vs. forecast targets  |

### Orders

| Method | Path                          | Description                   |
| ------ | ----------------------------- | ----------------------------- |
| GET    | /orders/                      | List all orders               |
| POST   | /orders/                      | Create a new order            |
| POST   | /orders/{order_id}/status     | Update order status           |
| GET    | /orders/{order_id}/timeline   | Full status change history    |

### SLA

| Method | Path                                  | Description                            |
| ------ | ------------------------------------- | -------------------------------------- |
| GET    | /sla/orders?status=&lens_type=        | SLA status for all orders (filterable) |

### Prediction

| Method | Path                    | Description                           |
| ------ | ----------------------- | ------------------------------------- |
| GET    | /prediction/orders      | Breach probability for all orders     |
| GET    | /prediction/high-risk   | Orders with breach probability ≥ 80%  |
| GET    | /prediction/summary     | Count of HIGH / MEDIUM / LOW orders   |

### Forecasting

| Method | Path               | Description                           |
| ------ | ------------------ | ------------------------------------- |
| GET    | /forecast/         | Retrieve stored forecasts             |
| POST   | /forecast/generate | Run model inference + save forecasts  |

### Dashboard

| Method | Path                | Description    |
| ------ | ------------------- | -------------- |
| GET    | /dashboard/summary  | KPI counts     |

### Alerts

| Method | Path      | Description                       |
| ------ | --------- | --------------------------------- |
| GET    | /alerts/  | All active alerts (stock + risk)  |

### Administration

| Method | Path                          | Description                               |
| ------ | ----------------------------- | ----------------------------------------- |
| POST   | /admin/seed-data              | Generate 500 sample orders + inventory    |
| POST   | /admin/train-model            | Build training dataset + train classifier |
| POST   | /admin/train-forecast-model   | Build forecast dataset + train regressor  |

---

## Installation

### Backend

Run from the project root:

```bash
pip install -r requirements.txt
cd backend
uvicorn app.main:app --reload
```

Backend URL: `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`

> **Note:** The backend must be started from the `backend/` directory. Model loading uses relative paths (`app/ml/*.pkl`) that resolve from that directory.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

---

## First-Run Setup (Required)

The prediction and forecast endpoints depend on trained models and seeded data. Run these steps once after first install using the Swagger UI at `http://localhost:8000/docs` or curl:

### Step 1 — Seed sample data

```bash
curl -X POST http://localhost:8000/admin/seed-data
```

Generates 500 orders, 162 inventory SKUs, and matching transactions. **Clears all existing data first.**

### Step 2 — Train the SLA breach model

```bash
curl -X POST http://localhost:8000/admin/train-model
```

Builds `training_data.csv` from live orders and trains `breach_model.pkl`.

### Step 3 — Train the inventory forecast model

```bash
curl -X POST http://localhost:8000/admin/train-forecast-model
```

Builds `forecast_training.csv` from transactions and trains `forecast_model.pkl`.

### Step 4 — Generate forecasts

```bash
curl -X POST http://localhost:8000/forecast/generate
```

Runs the forecast model against all distinct inventory SKUs and saves results to the database. Required for the Forecast dashboard and `inventory/health` to return data.

### Step 5 — Open the dashboard

Navigate to `http://localhost:5173`

> **Note:** Pre-trained `.pkl` files are included in the repository. Steps 1–4 only need to be re-run if you want to retrain on fresh data.

---

## Deploying to Production

### Backend — Render

The repo contains `render.yaml`. On [render.com](https://render.com):

1. **New → Web Service** → connect `Hs1000/ai-manufacturer`
2. Render auto-detects `render.yaml` (build + start commands pre-filled)
3. Click **Deploy**

The backend auto-seeds sample data and generates forecasts on first boot (empty DB detected via lifespan hook in `main.py`).

Live URL: `https://ai-manufacturer.onrender.com`

### Frontend — Vercel

The repo contains `frontend/vercel.json` (SPA rewrite rules) and `frontend/.env.production` (backend URL baked in at build time).

1. Go to [vercel.com](https://vercel.com) → **Add New Project** → import `Hs1000/ai-manufacturer`
2. Set **Root Directory** to `frontend`
3. Framework: **Vite** (auto-detected)
4. Click **Deploy** — no environment variables needed (`.env.production` is committed)

---

## Reviewer Notes

- **SQLite database** is stored at `backend/eyewear.db` and is created automatically on first start. It is not committed to the repo.
- **`requirements.txt`** lives at the project root, not inside `backend/`. Install it from the root before `cd backend`.
- **The backend must be launched from `backend/`**, not the repo root, because model loading uses relative paths like `app/ml/breach_model.pkl`.
- **Render ephemeral filesystem** — SQLite resets on every redeploy. The lifespan auto-seed in `main.py` handles this automatically.
- **Seed data is destructive** — `POST /admin/seed-data` deletes all existing orders, inventory, and transactions before regenerating.
- **Alert thresholds are hardcoded** in `alerts.py`: inventory quantity < 30 triggers LOW_STOCK; predicted demand > 10 triggers DEMAND_SPIKE; any order in QC status triggers HIGH_RISK_ORDER.
- **Recommended stock buffer** is hardcoded at 1.30× predicted demand in `forecast.py`.
- **Risk bucketing** (HIGH / MEDIUM / LOW) in `prediction.py` is a rule applied on top of the model's probability output — the underlying breach probability is fully model-driven (Random Forest `predict_proba`).
- **`/dashboard/order-status` and `/dashboard/forecast-demand`** listed in an earlier version of this README do not exist in the codebase. The only active dashboard endpoint is `/dashboard/summary`.

---

## Architecture Reference

See [ARCHITECTURE.md](ARCHITECTURE.md) and [ARCHITECTURE.pdf](ARCHITECTURE.pdf) for:
- Full system architecture diagram
- AI model selection rationale (why Random Forest, why no external API)
- Feature importance breakdown
- Alert threshold documentation

---

## Future Enhancements

* Time-series forecasting using Prophet or XGBoost
* Real-time notifications
* User authentication and role management
* Multi-warehouse inventory support
* Automated inventory replenishment recommendations
* LLM-powered operational insights
* Migrate from SQLite to PostgreSQL for persistent production data

---
