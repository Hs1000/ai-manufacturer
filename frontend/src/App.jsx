import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Navbar from "./components/Navbar";

import HomeDashboard from "./pages/HomeDashboard";
import OrderDashboard from "./pages/OrderDashboard";
import InventoryDashboard from "./pages/InventoryDashboard";
import ForecastDashboard from "./pages/ForecastDashboard";
import PredictionDashboard from "./pages/PredictionDashboard";
import AlertsDashboard from "./pages/AlertsDashboard";

function App() {

  return (

    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={
            <Navigate
              to="/dashboard"
            />
          }
        />

        <Route
          path="/dashboard"
          element={
            <HomeDashboard />
          }
        />

        <Route
          path="/orders"
          element={
            <OrderDashboard />
          }
        />

        <Route
          path="/inventory"
          element={
            <InventoryDashboard />
          }
        />

        <Route
          path="/forecast"
          element={
            <ForecastDashboard />
          }
        />

        <Route
          path="/predictions"
          element={
            <PredictionDashboard />
          }
        />

        <Route
          path="/alerts"
          element={
            <AlertsDashboard />
          }
        />

      </Routes>

    </BrowserRouter>

  );
}

export default App;