import React from "react";
import Plot from "react-plotly.js";

const TowerPlot = ({ coordinates = [], elements = [] }) => {
  if (!coordinates.length || !elements.length) {
    return <p className="text-red-400">⚠️ No section data to display.</p>;
  }

  // Unique nodes for red dots
  const uniqueNodes = new Set();
  coordinates.forEach(section => {
    Object.values(section).forEach(point => {
      if (Array.isArray(point)) {
        uniqueNodes.add(JSON.stringify(point));
      }
    });
  });
  const nodeCoords = Array.from(uniqueNodes).map(p => JSON.parse(p));
  const xNodes = nodeCoords.map(p => p[0]);
  const yNodes = nodeCoords.map(p => p[1]);

  // Plot structure lines
  const structureTraces = [];
  const sectionColors = ["red", "white"];

  elements.forEach((section, sectionIndex) => {
    const color = sectionColors[sectionIndex % sectionColors.length];
    section.elements.forEach((elem) => {
      const x = [elem.node_i[0], elem.node_j[0]];
      const y = [elem.node_i[1], elem.node_j[1]];
      structureTraces.push({
        x,
        y,
        mode: "lines",
        line: { color, width: 2 },
        type: "scatter",
        showlegend: false
      });
    });
  });

  // Red node dots
  const nodeTrace = {
    x: xNodes,
    y: yNodes,
    mode: "markers",
    type: "scatter",
    marker: { color: "red", size: 6 },
    showlegend: false
  };

  return (
    <Plot
      data={[...structureTraces, nodeTrace]}
      layout={{
        title: "📊 Tower Structure Plot",
        paper_bgcolor: "#1f2937",
        plot_bgcolor: "#1f2937",
        font: { color: "white" },
        xaxis: {
          showgrid: true,
          gridcolor: "#FFCC99",
          zeroline: false
        },
        yaxis: {
          showgrid: true,
          gridcolor: "#FFCC99",
          scaleanchor: "x",
          scaleratio: 1,
          zeroline: false
        },
        margin: { l: 10, r: 10, t: 40, b: 10 },
        height: 500
      }}
      config={{ responsive: true }}
      style={{ width: "100%", height: "100%" }}
    />
  );
};

export default TowerPlot;
