import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerPlot from "../components/TowerPlot";
import axios from "axios";
import "../results.css";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { towerData, sectionData: initialSectionData } = location.state || {};

  const [activeTab, setActiveTab] = useState("tower");
  const [sectionData, setSectionData] = useState(initialSectionData || {});
  const [elementSections, setElementSections] = useState({});
  const [sectionLibrary, setSectionLibrary] = useState({ round: [], angular: [] });

  // Load section profile library from backend
  useEffect(() => {
    axios
      .get("/api/sections/library")
      .then((res) => {
        console.log("📦 Section Library:", res.data);  // <-- You must see this!
        setSectionLibrary(res.data);
      })
      .catch((err) => {
        console.error("❌ Failed to load section library:", err);  // <-- Or this!
        setSectionLibrary({ round: [], angular: [] });
      });
  }, []);
  

  // Initialize dropdown state for each section and element
  useEffect(() => {
    if (sectionData?.data?.coordinates) {
      const init = {};
      sectionData.data.coordinates.forEach((coord) => {
        const sec = coord.section.toString();
        init[sec] = {
          M1: "", M2: "", M3: "", M4: "",
          D1: "", D2: "", D3: "", D4: "",
          C1: "", C2: ""
        };
      });
      setElementSections(init);
    }
  }, [sectionData]);

  // Handle recalculation with assigned section profiles
  const handleRecalculate = async () => {
    try {
      const res = await axios.post("/api/sections/generate", {
        towerData,
        elementSections
      });

      const updated = res.data;
      console.log("✅ Recalculated section:", updated);
      setSectionData({ data: updated });

      alert("✅ Tower section updated with assigned profiles!");
    } catch (err) {
      console.error("❌ Failed to recalculate:", err);
      alert("❌ Error while recalculating section.");
    }
  };

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

      <div className="flex justify-center mb-4 space-x-4">
        <button
          onClick={() => setActiveTab("tower")}
          className={`px-4 py-2 rounded font-bold ${
            activeTab === "tower" ? "bg-blue-600" : "bg-gray-700 hover:bg-gray-600"
          }`}
        >
          Tower Input
        </button>
        <button
          onClick={() => setActiveTab("section")}
          className={`px-4 py-2 rounded font-bold ${
            activeTab === "section" ? "bg-blue-600" : "bg-gray-700 hover:bg-gray-600"
          }`}
        >
          Section Geometry
        </button>
      </div>

      <div className="results-columns">
        {/* Left: Dropdown UI */}
        <div className="dropdown-box">
          <h2 className="text-xl font-semibold mb-4">🧰 Define Element Sections</h2>
          {sectionData.data?.coordinates?.map((coord) => {
            const sec = coord.section.toString();
            return (
              <div key={sec} className="bg-neutral-800 p-4 mb-4 rounded">
                <h4 className="font-bold text-white mb-2">Section {sec}</h4>
                {Object.keys(elementSections?.[sec] || {}).map((el) => (
                  <div key={el} className="flex items-center mb-2">
                    <label className="w-12 text-white">{el}</label>
                    <select
                      className="flex-1 bg-gray-700 text-white rounded px-2 py-1"
                      value={elementSections[sec][el]}
                      onChange={(e) => {
                        const updated = { ...elementSections };
                        updated[sec][el] = e.target.value;
                        setElementSections(updated);
                      }}
                    >
                      <option value="">Default (2” pipe)</option>
                      {sectionLibrary?.round?.length > 0 && (
                        <optgroup label="Round">
                          {sectionLibrary.round.map((opt) => (
                            <option key={opt.name} value={opt.name}>
                              {opt.name}
                            </option>
                          ))}
                        </optgroup>
                      )}
                      {sectionLibrary?.angular?.length > 0 && (
                        <optgroup label="Angular">
                          {sectionLibrary.angular.map((opt) => (
                            <option key={opt.name} value={opt.name}>
                              {opt.name}
                            </option>
                          ))}
                        </optgroup>
                      )}
                    </select>
                  </div>
                ))}
              </div>
            );
          })}

          {/* Recalculate button */}
          <button
            onClick={handleRecalculate}
            className="w-full mt-4 px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-black font-bold rounded"
          >
            🔄 Recalculate Section with Assigned Elements
          </button>
        </div>

        {/* Center: Tower Plot */}
        <div className="plot-box">
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

        {/* Right: JSON */}
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
            <button className="back-btn" onClick={() => navigate("/")}>
              🔙 Back to Form
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
