import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerScene from "../components/TowerScene";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // ✅ Extract both tower and section data from navigation state
  const { towerData, sectionData } = location.state || {};

  if (!towerData || !sectionData) {
    return (
      <div className="results-fallback">
        <div className="fallback-content">
          <p>🚫 No tower or section data available.</p>
          <button onClick={() => navigate("/")}>Go Back</button>
        </div>
      </div>
    );
  }

  return (
    <div className="results-container">
      <h1 className="results-heading">
        📡 Tower JSON Result – {towerData.tower_id}
      </h1>

      <div className="results-body">
        <div className="json-column">
          <h2 className="text-lg font-semibold">📄 Tower Input Data</h2>
          <pre className="json-box">
            {JSON.stringify(towerData, null, 2)}
          </pre>

          <h2 className="text-lg font-semibold mt-6">🧩 Section Geometry Data</h2>
          <pre className="json-box bg-gray-800">
            {JSON.stringify(sectionData, null, 2)}
          </pre>

          <div className="button-row">
            <button
              onClick={() =>
                navigator.clipboard.writeText(JSON.stringify(sectionData, null, 2))
              }
            >
              📋 Copy Section JSON
            </button>
            <button onClick={() => navigate("/")}>🔙 Back to Form</button>
          </div>
        </div>

        <div className="scene-column">
          <TowerScene geometry={sectionData} />
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
