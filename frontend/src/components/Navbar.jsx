import {
    Link,
    useLocation
  } from "react-router-dom";
  
  function Navbar() {
  
    const location =
      useLocation();
  
    const linkStyle =
      (path) => ({
  
        color:
          location.pathname === path
            ? "#60a5fa"
            : "white",
  
        textDecoration: "none",
  
        fontWeight: "600",
  
        fontSize: "16px"
  
      });
  
    return (
  
      <nav
        style={{
          background: "#1e293b",
          padding: "18px 32px",
          display: "flex",
          justifyContent:
            "space-between",
          alignItems: "center"
        }}
      >
  
        <h2
          style={{
            color: "white",
            margin: 0
          }}
        >
          AI Eyewear OMS
        </h2>
  
        <div
          style={{
            display: "flex",
            gap: "25px"
          }}
        >
  
          <Link
            to="/dashboard"
            style={
              linkStyle(
                "/dashboard"
              )
            }
          >
            Dashboard
          </Link>
  
          <Link
            to="/orders"
            style={
              linkStyle("/orders")
            }
          >
            Orders
          </Link>
  
          <Link
            to="/inventory"
            style={
              linkStyle(
                "/inventory"
              )
            }
          >
            Inventory
          </Link>
  
          <Link
            to="/forecast"
            style={
              linkStyle(
                "/forecast"
              )
            }
          >
            Forecast
          </Link>
  
          <Link
            to="/predictions"
            style={
              linkStyle(
                "/predictions"
              )
            }
          >
            AI Predictions
          </Link>

          <Link
            to="/alerts"
            style={
              linkStyle("/alerts")
            }
          >
            Alerts
          </Link>

        </div>
  
      </nav>
  
    );
  }
  
  export default Navbar;