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
    cross_section: "square",
    exposure_category: "",
    importance_factor: "",
    wind_speed_service: "",
    wind_speed_ultimate: ""
  });

  const navigate = useNavigate();

  // ✅ Update tower_id dynamically when height changes
  useEffect(() => {
    if (formData.height) {
      setFormData((prevData) => ({
        ...prevData,
        tower_id: `tower_${formData.height}`
      }));
    }
  }, [formData.height]);

  // ✅ Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  // ✅ Submit form and redirect
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting Tower Data:", formData);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/towers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const result = await response.json();

      if (response.ok) {
        navigate("/results", { state: { towerData: formData } });
      } else {
        alert(result.error || "Failed to submit tower data.");
      }
    } catch (error) {
      console.error("Error submitting tower data:", error);
      alert("Failed to submit tower data.");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 p-6 rounded-xl shadow-lg w-full max-w-3xl">
        <h1 className="text-2xl font-bold text-center mb-4">📡 Tower Design Input</h1>

        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold">Tower Base Width (m):</label>
            <input type="number" name="tower_base_width" value={formData.tower_base_width} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Top Width (m):</label>
            <input type="number" name="top_width" value={formData.top_width} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Height (m):</label>
            <input type="number" name="height" value={formData.height} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Variable Segments:</label>
            <input type="number" name="variable_segments" value={formData.variable_segments} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Constant Segments:</label>
            <input type="number" name="constant_segments" value={formData.constant_segments} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Cross Section:</label>
            <select name="cross_section" value={formData.cross_section} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500">
              <option value="square">Square</option>
              <option value="triangular">Triangular</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold">Exposure Category:</label>
            <input type="text" name="exposure_category" value={formData.exposure_category} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Importance Factor:</label>
            <input type="number" name="importance_factor" value={formData.importance_factor} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Basic Wind Speed (Service):</label>
            <input type="number" name="wind_speed_service" value={formData.wind_speed_service} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div>
            <label className="block text-sm font-semibold">Basic Wind Speed (Ultimate):</label>
            <input type="number" name="wind_speed_ultimate" value={formData.wind_speed_ultimate} onChange={handleChange}
              className="w-full p-2 rounded bg-gray-700 border border-gray-600 focus:ring focus:ring-blue-500" required />
          </div>

          <div className="col-span-2 text-center">
            <button type="submit"
              className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow-lg">
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
