function DataTable({
    headers,
    rows
  }) {
    return (
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
            borderCollapse: "collapse"
          }}
        >
          <thead>
            <tr
              style={{
                background:
                  "#f1f5f9"
              }}
            >
              {headers.map(
                (header) => (
                  <th
                    key={header}
                    style={{
                      padding:
                        "16px",
                      textAlign:
                        "center"
                    }}
                  >
                    {header}
                  </th>
                )
              )}
            </tr>
          </thead>
  
          <tbody>
  
            {rows}
  
          </tbody>
  
        </table>
      </div>
    );
  }
  
  export default DataTable;