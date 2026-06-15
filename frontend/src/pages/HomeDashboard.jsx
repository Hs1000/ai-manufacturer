import { useEffect, useState } from "react";
import api from "../api/api";
import DashboardContainer from "../components/DashboardContainer";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend
} from "recharts";

const COLORS = [
  "#3b82f6",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#06b6d4",
  "#ec4899",
  "#84cc16"
];

function HomeDashboard() {

  const [summary, setSummary] =
    useState(null);

  const [orderStatus, setOrderStatus] =
    useState([]);

  const [forecastData, setForecastData] =
    useState([]);

  useEffect(() => {

    fetchSummary();
    fetchOrderStatus();
    fetchForecastData();

  }, []);

  const fetchSummary = async () => {

    try {

      const response =
        await api.get(
          "/dashboard/summary"
        );

      setSummary(
        response.data
      );

    } catch (error) {

      console.error(
        "Summary Error",
        error
      );

    }
  };

  const fetchOrderStatus = async () => {

    try {

      const response =
        await api.get(
          "/dashboard/order-status"
        );

      setOrderStatus(
        response.data
      );

    } catch (error) {

      console.error(
        "Order Status Error",
        error
      );

    }
  };

  const fetchForecastData = async () => {

    try {

      const response =
        await api.get(
          "/dashboard/forecast-demand"
        );

      setForecastData(
        response.data
      );

    } catch (error) {

      console.error(
        "Forecast Error",
        error
      );

    }
  };

  if (!summary) {

    return (

      <DashboardContainer
        title="Executive Dashboard"
      >

        Loading...

      </DashboardContainer>

    );
  }

  return (

    <DashboardContainer
      title="Executive Dashboard"
    >

      {/* KPI CARDS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

        <Card
          title="Total Orders"
          value={
            summary.total_orders
          }
        />

        <Card
          title="Inventory SKUs"
          value={
            summary.inventory_skus
          }
        />

        <Card
          title="Forecast Records"
          value={
            summary.forecast_records
          }
        />

        <Card
          title="High Risk Orders"
          value={
            summary.high_risk_orders
          }
        />

        <Card
          title="SLA Breaches"
          value={
            summary.sla_breaches
          }
        />

      </div>

      {/* CHARTS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "1fr 1fr",
          gap: "25px"
        }}
      >

        {/* ORDER STATUS */}

        <div
          style={chartCard}
        >

          <h3
            style={chartTitle}
          >
            Order Status Distribution
          </h3>

          <ResponsiveContainer
            width="100%"
            height={320}
          >

            <PieChart>

              <Pie
                data={orderStatus}
                dataKey="count"
                nameKey="status"
                outerRadius={110}
                label
              >

                {orderStatus.map(
                  (_, index) => (

                    <Cell
                      key={index}
                      fill={
                        COLORS[
                          index %
                            COLORS.length
                        ]
                      }
                    />

                  )
                )}

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        </div>

        {/* FORECAST CHART */}

        <div
          style={chartCard}
        >

          <h3
            style={chartTitle}
          >
            Forecast Demand
          </h3>

          <ResponsiveContainer
            width="100%"
            height={320}
          >

            <BarChart
              data={
                forecastData
              }
            >

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="lens_type"
              />

              <YAxis />

              <Tooltip />

              <Legend />

              <Bar
                dataKey="predicted_demand"
                name="Predicted Demand"
                fill="#3b82f6"
              />

            </BarChart>

          </ResponsiveContainer>

        </div>

      </div>

    </DashboardContainer>

  );
}

function Card({
  title,
  value
}) {

  return (

    <div
      style={{
        background: "white",
        borderRadius: "14px",
        padding: "25px",
        textAlign: "center",
        boxShadow:
          "0 4px 12px rgba(0,0,0,0.08)"
      }}
    >

      <h3
        style={{
          marginBottom: "15px",
          color: "#475569"
        }}
      >
        {title}
      </h3>

      <h1
        style={{
          margin: 0,
          color: "#0f172a"
        }}
      >
        {value}
      </h1>

    </div>

  );
}

const chartCard = {

  background: "white",

  borderRadius: "14px",

  padding: "20px",

  boxShadow:
    "0 4px 12px rgba(0,0,0,0.08)"
};

const chartTitle = {

  textAlign: "center",

  marginBottom: "10px",

  color: "#334155"
};

export default HomeDashboard;