import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerPlot from "../components/TowerPlot"; // ✅ Make sure this is correctly imported

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { towerData, sectionData } = location.state || {};

  const [activeTab, setActiveTab] = useState("tower");

  // ✅ Debugging state
  useEffect(() => {
    console.log("📦 ResultsPage state:", { towerData, sectionData });
    console.log("🧩 Section Coordinates:", sectionData?.data?.coordinates);
    console.log("🧩 Section Elements:", sectionData?.data?.elements);
  }, []);

  // ✅ Fallback if state not passed
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

      {/* JSON Viewer */}
      <div className="bg-gray-800 rounded-xl p-4 shadow max-w-5xl mx-auto">
        <h2 className="text-xl font-semibold mb-2">{jsonData.title}</h2>
        <pre className="bg-gray-700 rounded p-3 overflow-x-auto max-h-[70vh]">
          {JSON.stringify(jsonData.data, null, 2)}
        </pre>
      </div>

      {/* Buttons */}
      <div className="flex justify-center mt-6 gap-4">
        <button
          className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded font-bold"
          onClick={() =>
            navigator.clipboard.writeText(
              JSON.stringify(jsonData.data, null, 2)
            )
          }
        >
          📋 Copy JSON
        </button>
        <button
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded font-bold"
          onClick={() => navigate("/")}
        >
          🔙 Back to Form
        </button>
      </div>

      <h2 className="text-xl font-semibold text-center mt-10 mb-2">📊 Tower Plot</h2>
      <div className="w-full h-[600px] bg-gray-800 rounded-xl p-2 flex justify-center items-center">
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
  );
};

export default ResultsPage;
