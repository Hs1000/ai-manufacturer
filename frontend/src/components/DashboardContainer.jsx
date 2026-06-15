function DashboardContainer({
    title,
    children
  }) {
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
            {title}
          </h1>
  
          {children}
  
        </div>
      </div>
    );
  }
  
  export default DashboardContainer;