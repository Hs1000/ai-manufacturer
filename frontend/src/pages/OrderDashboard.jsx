import { useEffect, useState } from "react";
import api from "../api/api";
import SummaryCards from "../components/SummaryCards";

function OrderDashboard() {
  const [orders, setOrders] = useState([]);

  const [status, setStatus] = useState("");
  const [lensType, setLensType] = useState("");

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    let url = "/sla/orders";

    const params = [];

    if (status) {
      params.push(`status=${status}`);
    }

    if (lensType) {
      params.push(`lens_type=${lensType}`);
    }

    if (params.length > 0) {
      url += "?" + params.join("&");
    }

    const response = await api.get(url);

    setOrders(response.data);
  };

  return (
    <div
      style={{
        background: "#f8fafc",
        minHeight: "100vh",
        padding: "30px"
      }}
    >
      <div
        style={{
          maxWidth: "1400px",
          margin: "0 auto"
        }}
      >
        <h1
          style={{
            textAlign: "center",
            fontSize: "48px",
            marginBottom: "40px"
          }}
        >
          Order Dashboard
        </h1>

        <SummaryCards orders={orders} />

        <div
          style={{
            background: "white",
            padding: "20px",
            borderRadius: "12px",
            marginBottom: "30px",
            display: "flex",
            justifyContent: "center",
            gap: "15px",
            boxShadow:
              "0 4px 12px rgba(0,0,0,0.08)"
          }}
        >
          <select
            value={status}
            onChange={(e) =>
              setStatus(e.target.value)
            }
            style={{
              padding: "10px",
              minWidth: "180px"
            }}
          >
            <option value="">
              All Statuses
            </option>

            <option value="QC">
              QC
            </option>

            <option value="COATING">
              COATING
            </option>

            <option value="DELIVERED">
              DELIVERED
            </option>
          </select>

          <select
            value={lensType}
            onChange={(e) =>
              setLensType(e.target.value)
            }
            style={{
              padding: "10px",
              minWidth: "180px"
            }}
          >
            <option value="">
              All Lens Types
            </option>

            <option value="Progressive">
              Progressive
            </option>

            <option value="Single Vision">
              Single Vision
            </option>

            <option value="Blue Light">
              Blue Light
            </option>
          </select>

          <button
            onClick={fetchOrders}
            style={{
              background: "#2563eb",
              color: "white",
              border: "none",
              padding:
                "10px 20px",
              borderRadius: "8px",
              cursor: "pointer"
            }}
          >
            Apply Filters
          </button>
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
                  Hours Remaining
                </th>
                <th style={thStyle}>
                  Health
                </th>
              </tr>
            </thead>

            <tbody>
              {orders.map(
                (order) => (
                  <tr
                    key={
                      order.order_id
                    }
                  >
                    <td style={tdStyle}>
                      {
                        order.order_number
                      }
                    </td>

                    <td style={tdStyle}>
                      {
                        order.lens_type
                      }
                    </td>

                    <td style={tdStyle}>
                      {order.status}
                    </td>

                    <td
                      style={{
                        ...tdStyle,
                        color:
                          order.hours_remaining <
                          0
                            ? "#dc2626"
                            : "#16a34a",
                        fontWeight:
                          "600"
                      }}
                    >
                      {
                        order.hours_remaining
                      }
                    </td>

                    <td style={tdStyle}>
                      {order.breached ? (
                        <span>
                          🔴 Breached
                        </span>
                      ) : (
                        <span>
                          🟢 Healthy
                        </span>
                      )}
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>
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

export default OrderDashboard;