import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerScene from "../components/TowerScene";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const towerData = location.state?.towerData;

  if (!towerData) {
    return (
      <div className="results-fallback">
        <div className="fallback-content">
          <p>No tower data available.</p>
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
          <pre className="json-box">
            {JSON.stringify(towerData, null, 2)}
          </pre>

          <div className="button-row">
            <button
              onClick={() =>
                navigator.clipboard.writeText(JSON.stringify(towerData, null, 2))
              }
            >
              📋 Copy JSON
            </button>
            <button onClick={() => navigate("/")}>🔙 Back to Form</button>
          </div>
        </div>

        <div className="scene-column">
          <TowerScene />
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
