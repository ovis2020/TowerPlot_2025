import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TowerForm from "./components/TowerForm";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-900 text-white p-4">
        <Routes>
          <Route path="/" element={<TowerForm />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
