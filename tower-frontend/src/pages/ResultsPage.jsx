import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const towerData = location.state?.towerData;

  if (!towerData) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white px-4">
        <p className="text-lg mb-4">❌ No tower data found.</p>
        <button
          onClick={() => navigate("/")}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
        >
          🔙 Go Back to Form
        </button>
      </div>
    );
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(towerData, null, 2));
    alert("✅ JSON copied to clipboard!");
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-4">
        📡 Tower JSON Result – <span className="text-blue-400">{towerData.tower_id}</span>
      </h1>

      <div className="flex flex-col sm:flex-row sm:justify-between items-start sm:items-center mb-4">
        <button
          onClick={handleCopy}
          className="mb-4 sm:mb-0 px-4 py-2 bg-green-600 hover:bg-green-700 rounded"
        >
          📋 Copy JSON
        </button>

        <button
          onClick={() => navigate("/")}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
        >
          🔙 Back to Form
        </button>
      </div>

      <pre className="bg-gray-800 p-4 rounded overflow-x-auto text-sm whitespace-pre-wrap">
        {JSON.stringify(towerData, null, 2)}
      </pre>
    </div>
  );
};

export default ResultsPage;
