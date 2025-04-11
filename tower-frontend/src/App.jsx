import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TowerForm from "./components/TowerForm";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <Router>
      <Routes>
        {/* Centered layout for TowerForm */}
        <Route
          path="/"
          element={
            <div className="flex items-center justify-center min-h-screen bg-gray-900 text-white p-4">
              <TowerForm />
            </div>
          }
        />

        {/* Full layout for results page */}
        <Route path="/results" element={<ResultsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
