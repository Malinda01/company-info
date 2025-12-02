import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState([]);

  const uploadCSV = async () => {
    const form = new FormData();
    form.append("file", file);

    const res = await axios.post("http://localhost:5000/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    setResult(res.data.data);
  };

  const containerStyle = {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f5f7fa",
    padding: "20px",
  };

  const cardStyle = {
    width: "100%",
    maxWidth: "720px",
    background: "#fff",
    padding: "32px",
    borderRadius: "8px",
    boxShadow: "0 8px 24px rgba(0,0,0,0.08)",
    textAlign: "center",
  };

  const controlsStyle = {
    display: "flex",
    gap: "12px",
    alignItems: "center",
    justifyContent: "center",
    marginTop: "12px",
    marginBottom: "20px",
    flexWrap: "wrap",
  };

  const inputStyle = {
    padding: "8px 12px",
    borderRadius: "6px",
    border: "1px solid #d0d7de",
    background: "#fff",
  };

  const buttonStyle = {
    padding: "9px 16px",
    borderRadius: "6px",
    border: "none",
    background: "#0366d6",
    color: "#fff",
    cursor: "pointer",
  };

  const preStyle = {
    textAlign: "left",
    maxHeight: "320px",
    overflow: "auto",
    background: "#f6f8fa",
    padding: "12px",
    borderRadius: "6px",
    border: "1px solid #e1e4e8",
  };

  return (
    <div style={containerStyle}>
      <div style={cardStyle}>
        <h1 style={{ margin: 0 }}>Company Data</h1>

        <div style={controlsStyle}>
          <input
            style={inputStyle}
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            style={buttonStyle}
            onClick={uploadCSV}
            disabled={!file}
            title={!file ? "Choose a CSV file first" : "Upload & Process"}
          >
            Upload & Process
          </button>
        </div>

        <h2 style={{ marginBottom: "8px" }}>Results</h2>

        <pre style={preStyle}>{JSON.stringify(result, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
