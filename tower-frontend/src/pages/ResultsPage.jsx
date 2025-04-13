import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TowerPlot from "../components/TowerPlot";
import axios from "axios";
import "../results.css";

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const storedTowerData = JSON.parse(localStorage.getItem("towerData"));
  const storedSectionData = JSON.parse(localStorage.getItem("sectionData"));

  const { towerData: navTowerData, sectionData: navSectionData } = location.state || {};
  const towerData = navTowerData || storedTowerData;
  const initialSectionData = navSectionData || storedSectionData;

  const [activeTab, setActiveTab] = useState("tower");
  const [sectionData, setSectionData] = useState(initialSectionData || {});
  const [elementSections, setElementSections] = useState({});
  const [sectionLibrary, setSectionLibrary] = useState({ round: [], angular: [] });

  useEffect(() => {
    axios
      .get("/api/sections/library")
      .then((res) => {
        console.log("📦 Section Library:", res.data);
        setSectionLibrary(res.data);
      })
      .catch((err) => {
        console.error("❌ Failed to load section library:", err);
        setSectionLibrary({ round: [], angular: [] });
      });
  }, []);

  useEffect(() => {
    if (sectionData?.data?.coordinates) {
      setElementSections((prev) => {
        const updated = { ...prev };
        sectionData.data.coordinates.forEach((coord) => {
          const sec = coord.section.toString();
          if (!updated[sec]) {
            updated[sec] = { M: "", D: "", C: "" };
          }
        });
        return updated;
      });
    }
  }, [sectionData]);
  

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

  const handleSaveFinalSection = async () => {
    console.log("🧠 towerData at save time:", towerData);

    if (!towerData) {
      alert("⚠️ towerData is missing. Cannot save.");
      return;
    }

    console.log("📦 Sending to backend:", {
      towerData,
      elementSections
    });

    try {
      const res = await axios.post(`/api/calculate/section/${towerData.tower_id}`, {
        towerData,
        elementSections
      });

      alert("✅ Final section saved to cloud storage.");
      console.log("🗂️ Saved:", res.data.url);
    } catch (err) {
      console.error("❌ Failed to save section:", err);
      alert(err.response?.data?.error || "❌ Error saving section");
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
        <div className="dropdown-box">
          <h2 className="text-xl font-semibold mb-4">🧰 Define Element Sections</h2>
          {sectionData.data?.coordinates?.map((coord) => {
            const sec = coord.section.toString();
            return (
              <div key={sec} className="bg-neutral-800 p-4 mb-4 rounded">
                <h4 className="font-bold text-white mb-2">Section {sec}</h4>
                {["M", "D", "C"].map((group) => (
                  <div key={group} className="flex items-center mb-2">
                    <label className="w-24 text-white">
                      {group === "M" ? "Legs (M)" : group === "D" ? "Diagonals (D)" : "Horizontals (C)"}
                    </label>
                    <select
                      className="flex-1 bg-gray-700 text-white rounded px-2 py-1"
                      value={elementSections[sec]?.[group] || ""}
                      onChange={(e) => {
                        const updated = { ...elementSections };
                        updated[sec] = { ...updated[sec], [group]: e.target.value };
                        setElementSections(updated);
                      }}
                    >
                      <option value="">Default (2” pipe)</option>
                      {sectionLibrary?.round?.length > 0 && (
                        <optgroup label="Round">
                          {sectionLibrary.round.map((opt) => (
                            <option key={opt.name} value={opt.name}>{opt.name}</option>
                          ))}
                        </optgroup>
                      )}
                      {sectionLibrary?.angular?.length > 0 && (
                        <optgroup label="Angular">
                          {sectionLibrary.angular.map((opt) => (
                            <option key={opt.name} value={opt.name}>{opt.name}</option>
                          ))}
                        </optgroup>
                      )}
                    </select>
                  </div>
                ))}
              </div>
            );
          })}

          <button
            onClick={handleRecalculate}
            className="w-full mt-4 px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-black font-bold rounded"
          >
            🔄 Recalculate Section with Assigned Elements
          </button>

          <button
            onClick={handleSaveFinalSection}
            className="w-full mt-4 px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-bold rounded"
          >
            💾 Save Final JSON to Cloud
          </button>
        </div>

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
