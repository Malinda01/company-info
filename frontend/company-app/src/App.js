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

  return (
    <div style={{ padding: "40px" }}>
      <h1>Company Info Extractor</h1>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadCSV} style={{ marginLeft: "10px" }}>
        Upload & Process
      </button>

      <h2>Results</h2>

      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default App;
