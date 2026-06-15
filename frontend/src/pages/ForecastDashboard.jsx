import {
    useEffect,
    useState
  } from "react";
  
  import api from "../api/api";
  
  import DashboardContainer
  from "../components/DashboardContainer";
  
  import DataTable
  from "../components/DataTable";
  
  function ForecastDashboard() {
  
    const [forecasts,
      setForecasts] =
        useState([]);
  
    useEffect(() => {
  
      fetchForecasts();
  
    }, []);
  
    const fetchForecasts =
      async () => {
  
      const response =
        await api.get(
          "/forecast"
        );
  
      setForecasts(
        response.data
      );
    };
  
    return (
  
      <DashboardContainer
        title="Forecast Dashboard"
      >
  
        <DataTable
          headers={[
            "Lens Type",
            "Power",
            "Predicted Demand",
            "Recommended Stock"
          ]}
          rows={forecasts.map(
            (forecast) => (
  
              <tr
                key={forecast.id}
              >
  
                <td style={td}>
                  {
                    forecast.lens_type
                  }
                </td>
  
                <td style={td}>
                  {forecast.power}
                </td>
  
                <td style={td}>
                  {
                    forecast.predicted_demand
                  }
                </td>
  
                <td style={td}>
                  {
                    forecast.recommended_stock
                  }
                </td>
  
              </tr>
  
            )
          )}
        />
  
      </DashboardContainer>
  
    );
  }
  
  const td = {
    padding: "14px",
    textAlign: "center",
    borderBottom:
      "1px solid #f1f5f9"
  };
  
  export default ForecastDashboard;