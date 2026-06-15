import {
    useEffect,
    useState
  } from "react";
  
  import api from "../api/api";
  
  import DashboardContainer
    from "../components/DashboardContainer";
  
  
  function AlertsDashboard() {
  
    const [alerts, setAlerts] =
      useState([]);
  
    useEffect(() => {
  
      fetchAlerts();
  
    }, []);
  
    const fetchAlerts =
      async () => {
  
        const response =
          await api.get(
            "/alerts/"
          );
  
        setAlerts(
          response.data
        );
      };
  
    return (
  
      <DashboardContainer
        title="Alert Center"
      >
  
        <div
          style={{
            display: "flex",
            flexDirection:
              "column",
            gap: "16px"
          }}
        >
  
          {alerts.map(
            (
              alert,
              index
            ) => (
  
              <div
                key={index}
                style={{
                  background:
                    "white",
  
                  padding:
                    "18px",
  
                  borderRadius:
                    "12px",
  
                  boxShadow:
                    "0 4px 10px rgba(0,0,0,0.08)"
                }}
              >
  
                <h3>
  
                  {alert.severity ===
                  "HIGH"
                    ? "🔴"
  
                    : alert.severity ===
                      "MEDIUM"
                    ? "🟡"
  
                    : "🔵"}
  
                  {" "}
  
                  {alert.type}
  
                </h3>
  
                <p>
                  {
                    alert.message
                  }
                </p>
  
              </div>
  
            )
          )}
  
        </div>
  
      </DashboardContainer>
  
    );
  }
  
  export default AlertsDashboard;