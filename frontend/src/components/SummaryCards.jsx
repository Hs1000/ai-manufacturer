function Card({ title, value, color }) {
    return (
      <div
        style={{
          background: "white",
          borderRadius: "12px",
          padding: "24px",
          textAlign: "center",
          boxShadow: "0 4px 12px rgba(0,0,0,0.08)"
        }}
      >
        <h3
          style={{
            marginBottom: "10px",
            color: "#64748b"
          }}
        >
          {title}
        </h3>
  
        <h1
          style={{
            margin: 0,
            color: color
          }}
        >
          {value}
        </h1>
      </div>
    );
  }
  
  function SummaryCards({ orders }) {
    const totalOrders = orders.length;
  
    const activeOrders = orders.filter(
      (o) => o.status !== "DELIVERED"
    ).length;
  
    const breachedOrders = orders.filter(
      (o) => o.breached
    ).length;
  
    const qcOrders = orders.filter(
      (o) => o.status === "QC"
    ).length;
  
    return (
      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(220px, 1fr))",
          gap: "20px",
          marginBottom: "40px"
        }}
      >
        <Card
          title="Total Orders"
          value={totalOrders}
          color="#2563eb"
        />
  
        <Card
          title="Active Orders"
          value={activeOrders}
          color="#16a34a"
        />
  
        <Card
          title="Breached Orders"
          value={breachedOrders}
          color="#dc2626"
        />
  
        <Card
          title="QC Orders"
          value={qcOrders}
          color="#7c3aed"
        />
      </div>
    );
  }
  
  export default SummaryCards;