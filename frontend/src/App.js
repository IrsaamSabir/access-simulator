import React, { useState } from "react";

function App() {
  const [employees, setEmployees] = useState([
    { id: "", access_level: 0, request_time: "", room: "ServerRoom" }
  ]);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (index, field, value) => {
    const newEmployees = [...employees];
    newEmployees[index][field] =
      field === "access_level" ? parseInt(value || 0, 10) : value;
    setEmployees(newEmployees);
  };

  const addEmployee = () => {
    setEmployees([
      ...employees,
      { id: "", access_level: 0, request_time: "", room: "ServerRoom" }
    ]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResults(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/simulate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ employees }),
      });

      if (!response.ok) {
        const text = await response.text();
        setError(`Server error: ${response.status}\n${text}`);
        return;
      }

      const data = await response.json();
      setResults(data.results || []);
    } catch (err) {
      setError("Network error: " + err.message);
    }
  };

  return (
    <div style={{
      fontFamily: "Arial, sans-serif",
      backgroundColor: "#f9f9f9",
      minHeight: "100vh",
      padding: "30px"
    }}>
      <h2 style={{ textAlign: "center", color: "#333" }}>Access Simulator</h2>

      {employees.map((emp, index) => (
        <div key={index} style={{
          background: "white",
          padding: "15px",
          marginBottom: "15px",
          borderRadius: "10px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
          display: "grid",
          gridTemplateColumns: "1fr 1fr 1fr 1fr",
          gap: "10px"
        }}>
          <input
            placeholder="Employee ID"
            value={emp.id}
            onChange={(e) => handleChange(index, "id", e.target.value)}
            style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "6px" }}
          />
          <input
            type="number"
            placeholder="Access Level"
            value={emp.access_level || ""}
            onChange={(e) => handleChange(index, "access_level", e.target.value)}
            style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "6px" }}
          />
          <input
            type="text"
            placeholder="HH:MM"
            pattern="^([01]\\d|2[0-3]):([0-5]\\d)$"
            value={emp.request_time}
            onChange={(e) => handleChange(index, "request_time", e.target.value)}
            style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "6px" }}
          />
          <select
            value={emp.room}
            onChange={(e) => handleChange(index, "room", e.target.value)}
            style={{ padding: "8px", border: "1px solid #ccc", borderRadius: "6px" }}
          >
            <option value="ServerRoom">ServerRoom</option>
            <option value="Vault">Vault</option>
            <option value="R&D Lab">R&D Lab</option>
          </select>
        </div>
      ))}

      <div style={{ textAlign: "center", marginBottom: "20px" }}>
        <button
          onClick={addEmployee}
          style={{
            padding: "10px 20px",
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer"
          }}
        >
          Add Employee
        </button>
      </div>

      <div style={{ textAlign: "center" }}>
        <button
          onClick={handleSubmit}
          style={{
            padding: "12px 30px",
            backgroundColor: "#28a745",
            color: "white",
            border: "none",
            borderRadius: "6px",
            fontSize: "16px",
            cursor: "pointer"
          }}
        >
          Simulate Access
        </button>
      </div>

      {error && (
        <div style={{
          marginTop: "20px",
          padding: "15px",
          background: "#ffe0e0",
          border: "1px solid #ff4d4d",
          borderRadius: "6px",
          color: "#b30000",
          whiteSpace: "pre-wrap"
        }}>
          {error}
        </div>
      )}

      {results && results.length > 0 && (
        <div style={{
          marginTop: "30px",
          padding: "20px",
          background: "white",
          borderRadius: "10px",
          boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
        }}>
          <h3 style={{ color: "#333" }}>Results</h3>
          <table style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "10px"
          }}>
            <thead>
              <tr style={{ background: "#f4f4f4", textAlign: "left" }}>
                <th style={{ padding: "8px", borderBottom: "1px solid #ddd" }}>Employee ID</th>
                <th style={{ padding: "8px", borderBottom: "1px solid #ddd" }}>Status</th>
                <th style={{ padding: "8px", borderBottom: "1px solid #ddd" }}>Reason</th>
              </tr>
            </thead>
            <tbody>
              {results.map((res, idx) => (
                <tr key={idx}>
                  <td style={{ padding: "8px", borderBottom: "1px solid #eee" }}>{res.id}</td>
                  <td style={{ padding: "8px", borderBottom: "1px solid #eee" }}>{res.status}</td>
                  <td style={{ padding: "8px", borderBottom: "1px solid #eee" }}>{res.reason}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
