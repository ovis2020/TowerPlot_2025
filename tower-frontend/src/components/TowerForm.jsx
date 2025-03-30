import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const TowerForm = () => {
  const [formData, setFormData] = useState({
    tower_id: "",
    tower_base_width: "",
    top_width: "",
    height: "",
    variable_segments: "",
    constant_segments: "",
    cross_section: "",
    exposure_category: "",
    importance_factor: "",
    wind_speed_service: "",
    wind_speed_ultimate: ""
  });

  const navigate = useNavigate();

  // ✅ Dynamically update tower_id based on height
  useEffect(() => {
    if (formData.height) {
      setFormData((prev) => ({
        ...prev,
        tower_id: `tower_${formData.height}`
      }));
    }
  }, [formData.height]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("📤 Submitting tower data:", formData);

    try {
      // Step 1: Upload base data
      const towerRes = await fetch("http://127.0.0.1:5000/api/towers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const towerResult = await towerRes.json();

      if (!towerRes.ok) {
        alert(towerResult.error || "Failed to submit tower data.");
        return;
      }

      // Step 2: Calculate section geometry
      const sectionRes = await fetch(
        `http://127.0.0.1:5000/api/calculate/section/${formData.tower_id}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            "Tower Base Width": parseFloat(formData.tower_base_width),
            "Top Width": parseFloat(formData.top_width),
            "Height": parseFloat(formData.height),
            "Variable Segments": parseInt(formData.variable_segments),
            "Constant Segments": parseInt(formData.constant_segments)
          })
        }
      );

      const sectionResult = await sectionRes.json();

      if (!sectionRes.ok) {
        alert(sectionResult.error || "Section calculation failed.");
        return;
      }

      console.log("✅ Navigating with state:", {
        towerData: formData,
        sectionData: sectionResult
      });
      

      // Step 3: Navigate to /results with tower + section data
      navigate("/results", {
        state: {
          towerData: formData,
          sectionData: sectionResult
        }
      });
    } catch (error) {
      console.error("❌ Error:", error);
      alert("Something went wrong while submitting the form.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 p-6 rounded-xl shadow-lg w-full max-w-3xl">
        <h1 className="text-2xl font-bold text-center mb-4">📡 Tower Design Input</h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          {[
            { label: "Tower Base Width (m)", name: "tower_base_width" },
            { label: "Top Width (m)", name: "top_width" },
            { label: "Height (m)", name: "height" },
            { label: "Variable Segments", name: "variable_segments" },
            { label: "Constant Segments", name: "constant_segments" },
            { label: "Exposure Category", name: "exposure_category" },
            { label: "Importance Factor", name: "importance_factor" },
            { label: "Basic Wind Speed (Service)", name: "wind_speed_service" },
            { label: "Basic Wind Speed (Ultimate)", name: "wind_speed_ultimate" }
          ].map((field) => (
            <div key={field.name}>
              <label className="block text-sm font-semibold">{field.label}:</label>
              <input
                type="number"
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                required
                className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500"
              />
            </div>
          ))}

          <div>
            <label className="block text-sm font-semibold">Cross Section:</label>
            <select
              name="cross_section"
              value={formData.cross_section}
              onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500"
            >
              <option value="">-- Select --</option>
              <option value="square">Square</option>
              <option value="triangular">Triangular</option>
            </select>
          </div>

          <div className="col-span-2 text-center">
            <button
              type="submit"
              className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow-lg"
            >
              Submit 🚀
            </button>
          </div>
        </form>

        <p className="text-center text-sm mt-4">
          <strong>Generated Tower ID:</strong> {formData.tower_id}
        </p>
      </div>
    </div>
  );
};

export default TowerForm;
