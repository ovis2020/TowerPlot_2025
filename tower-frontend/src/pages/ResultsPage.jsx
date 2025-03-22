import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerScene from "../components/TowerScene";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const towerData = location.state?.towerData;

  if (!towerData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <div className="text-center">
          <p className="text-lg mb-4">No tower data available.</p>
          <button
            onClick={() => navigate("/")}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6">
        📡 Tower JSON Result – <span className="text-blue-400">{towerData.tower_id}</span>
      </h1>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* JSON Data Block */}
        <div className="lg:w-1/2 w-full">
          <pre className="bg-gray-800 p-4 rounded overflow-x-auto text-sm whitespace-pre-wrap">
            {JSON.stringify(towerData, null, 2)}
          </pre>
          <div className="mt-4 flex gap-2">
            <button
              onClick={() => navigator.clipboard.writeText(JSON.stringify(towerData, null, 2))}
              className="px-4 py-2 bg-orange-600 hover:bg-orange-700 rounded"
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
        </div>

        {/* 3D Scene Block */}
        <div className="lg:w-1/2 w-full h-[600px] bg-gray-800 rounded-lg overflow-hidden">
          <TowerScene />
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
