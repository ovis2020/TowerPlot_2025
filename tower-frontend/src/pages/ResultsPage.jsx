import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerPlot from "../components/TowerPlot";
import "../results.css";




const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { towerData, sectionData } = location.state || {};

  const [activeTab, setActiveTab] = useState("tower");

  useEffect(() => {
    console.log("📦 ResultsPage state:", { towerData, sectionData });
    console.log("🧩 Section Coordinates:", sectionData?.data?.coordinates);
    console.log("🧩 Section Elements:", sectionData?.data?.elements);
  }, []);

  if (!towerData || !sectionData) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
        <p className="mb-4 text-lg">🚫 No tower or section data available.</p>
        <button
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
          onClick={() => navigate("/")}
        >
          🔙 Back to Form
        </button>
      </div>
    );
  }

  const jsonData =
    activeTab === "tower"
      ? { title: "📄 Tower Input Data", data: towerData }
      : { title: "🧩 Section Geometry Data", data: sectionData };

  return (
    <div className="w-full min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold text-center mb-6">
        📡 Tower JSON Result – {towerData.tower_id}
      </h1>

      {/* Tabs */}
      <div className="flex justify-center mb-4 space-x-4">
        <button
          onClick={() => setActiveTab("tower")}
          className={`px-4 py-2 rounded font-bold ${
            activeTab === "tower"
              ? "bg-blue-600"
              : "bg-gray-700 hover:bg-gray-600"
          }`}
        >
          Tower Input
        </button>
        <button
          onClick={() => setActiveTab("section")}
          className={`px-4 py-2 rounded font-bold ${
            activeTab === "section"
              ? "bg-blue-600"
              : "bg-gray-700 hover:bg-gray-600"
          }`}
        >
          Section Geometry
        </button>
      </div>

      {/* Two-column layout (JSON + Plot) */}
      <div className="results-columns">
        {/* Left JSON panel */}
        <div className="panel-box">
          <h2 className="text-xl font-semibold mb-2">{jsonData.title}</h2>
          <pre className="json-preview">
            {JSON.stringify(jsonData.data, null, 2)}
          </pre>

          <div className="action-buttons">
            <button
              className="copy-btn"
              onClick={() =>
                navigator.clipboard.writeText(
                  JSON.stringify(jsonData.data, null, 2)
                )
              }
            >
              📋 Copy JSON
            </button>
            <button
              className="back-btn"
              onClick={() => navigate("/")}
            >
              🔙 Back to Form
            </button>
          </div>
        </div>

        {/* Right Plot panel */}
        <div className="flex-1 bg-gray-800 rounded-xl p-4 shadow-lg">
          <h2 className="text-xl font-semibold mb-2">📊 Tower Plot</h2>
          <div className="plot-container">
            {sectionData.data?.coordinates && sectionData.data?.elements ? (
              <TowerPlot
                coordinates={sectionData.data.coordinates}
                elements={sectionData.data.elements}
              />
            ) : (
              <p className="text-yellow-300">⚠️ No section data to display.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
