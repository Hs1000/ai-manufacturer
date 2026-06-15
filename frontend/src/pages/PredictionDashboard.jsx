import { useEffect, useState } from "react";
import api from "../api/api";
import DashboardContainer from "../components/DashboardContainer";

function PredictionDashboard() {

  const [predictions, setPredictions] =
    useState([]);

  const [summary, setSummary] =
    useState({
      high: 0,
      medium: 0,
      low: 0
    });

  useEffect(() => {

    fetchPredictions();
    fetchSummary();

  }, []);

  const fetchPredictions =
    async () => {

      const response =
        await api.get(
          "/prediction/orders"
        );

      setPredictions(
        response.data
      );
    };

  const fetchSummary =
    async () => {

      const response =
        await api.get(
          "/prediction/summary"
        );

      setSummary(
        response.data
      );
    };

  return (

    <DashboardContainer
      title="AI Breach Prediction Dashboard"
    >

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(3, 1fr)",
          gap: "20px",
          marginBottom: "30px"
        }}
      >

        <Card
          title="High Risk"
          value={summary.high}
          color="#dc2626"
        />

        <Card
          title="Medium Risk"
          value={summary.medium}
          color="#d97706"
        />

        <Card
          title="Low Risk"
          value={summary.low}
          color="#16a34a"
        />

      </div>

      <div
        style={{
          background: "white",
          borderRadius: "12px",
          overflow: "hidden",
          boxShadow:
            "0 4px 12px rgba(0,0,0,0.08)"
        }}
      >

        <table
          style={{
            width: "100%",
            borderCollapse:
              "collapse"
          }}
        >

          <thead>

            <tr
              style={{
                background:
                  "#f1f5f9"
              }}
            >

              <th style={thStyle}>
                Order
              </th>

              <th style={thStyle}>
                Lens Type
              </th>

              <th style={thStyle}>
                Status
              </th>

              <th style={thStyle}>
                Probability
              </th>

              <th style={thStyle}>
                Risk Level
              </th>

            </tr>

          </thead>

          <tbody>

            {predictions.map(
              (item) => (

                <tr
                  key={
                    item.order_id
                  }
                >

                  <td style={tdStyle}>
                    {
                      item.order_number
                    }
                  </td>

                  <td style={tdStyle}>
                    {
                      item.lens_type
                    }
                  </td>

                  <td style={tdStyle}>
                    {
                      item.status
                    }
                  </td>

                  <td style={tdStyle}>
                    {
                      Math.round(
                        item.breach_probability * 100
                      )
                    }%
                  </td>

                  <td style={tdStyle}>

                    {item.risk_level ===
                    "HIGH" ? (
                      <span>
                        🔴 HIGH
                      </span>
                    ) : item.risk_level ===
                      "MEDIUM" ? (
                      <span>
                        🟡 MEDIUM
                      </span>
                    ) : (
                      <span>
                        🟢 LOW
                      </span>
                    )}

                  </td>

                </tr>

              )
            )}

          </tbody>

        </table>

      </div>

    </DashboardContainer>

  );
}

function Card({
  title,
  value,
  color
}) {
  return (
    <div
      style={{
        background: "white",
        padding: "24px",
        borderRadius: "12px",
        textAlign: "center",
        boxShadow:
          "0 4px 12px rgba(0,0,0,0.08)"
      }}
    >
      <h3>{title}</h3>

      <h1
        style={{
          color
        }}
      >
        {value}
      </h1>
    </div>
  );
}

const thStyle = {
  padding: "16px",
  textAlign: "center",
  borderBottom:
    "1px solid #e2e8f0"
};

const tdStyle = {
  padding: "14px",
  textAlign: "center",
  borderBottom:
    "1px solid #f1f5f9"
};

export default PredictionDashboard;