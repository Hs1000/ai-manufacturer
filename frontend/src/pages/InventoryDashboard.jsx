import {
    useEffect,
    useState
  } from "react";
  
  import api from "../api/api";
  
  import DashboardContainer
  from "../components/DashboardContainer";
  
  import DataTable
  from "../components/DataTable";
  
  function InventoryDashboard() {
  
    const [inventory,
      setInventory] =
        useState([]);
  
    useEffect(() => {
  
      fetchInventory();
  
    }, []);
  
    const fetchInventory =
      async () => {
  
      const response =
        await api.get(
          "/inventory/health"
        );
  
      setInventory(
        response.data
      );
    };
  
    return (
  
      <DashboardContainer
        title="Inventory Dashboard"
      >
  
        <DataTable
          headers={[
            "Lens Type",
            "Current Stock",
            "Recommended",
            "Shortage",
            "Status"
          ]}
          rows={inventory.map(
            (item, index) => (
  
              <tr key={index}>
  
                <td style={td}>
                  {item.lens_type}
                </td>
  
                <td style={td}>
                  {item.current_stock}
                </td>
  
                <td style={td}>
                  {
                    item.recommended_stock
                  }
                </td>
  
                <td style={td}>
                  {item.shortage}
                </td>
  
                <td style={td}>
  
                  {item.status ===
                  "LOW_STOCK"
                    ? "🔴 LOW"
                    : item.status ===
                      "WARNING"
                    ? "🟡 WARNING"
                    : "🟢 HEALTHY"}
  
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
  
  export default InventoryDashboard;