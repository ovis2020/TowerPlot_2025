import React, { useEffect, useRef } from "react";
import Plot from "react-plotly.js";

const TowerPlot = ({ coordinates, elements }) => {
  const plotRef = useRef(null);

  if (!coordinates || !elements) return null;

  // Extract node points
  const nodeSet = new Set();
  coordinates.forEach((coord) => {
    Object.values(coord).forEach((pt) => {
      if (Array.isArray(pt)) nodeSet.add(pt.toString());
    });
  });

  const nodes = Array.from(nodeSet).map((pt) => pt.split(",").map(Number));
  const xNodes = nodes.map((n) => n[0]);
  const yNodes = nodes.map((n) => n[1]);

  // Plot lines
  const lineTraces = elements.map((section, i) => {
    const color = i % 2 === 0 ? "red" : "white";
    return section.elements.map((el) => ({
      x: [el.node_i[0], el.node_j[0]],
      y: [el.node_i[1], el.node_j[1]],
      mode: "lines",
      line: { color, width: 2 },
      type: "scatter",
      showlegend: false
    }));
  }).flat();

  const nodeTrace = {
    x: xNodes,
    y: yNodes,
    mode: "markers",
    marker: { color: "red", size: 6 },
    type: "scatter",
    showlegend: false
  };

  const layout = {
    autosize: true,
    margin: { l: 10, r: 10, t: 10, b: 10 },
    plot_bgcolor: "#1e293b",
    paper_bgcolor: "#1e293b",
    xaxis: {
      showgrid: true,
      gridcolor: "#FFCC99",
      dtick: 1
    },
    yaxis: {
      showgrid: true,
      gridcolor: "#FFCC99",
      dtick: 1,
      scaleanchor: "x",
      scaleratio: 1
    }
  };

  return (
    <Plot
      ref={plotRef}
      data={[...lineTraces, nodeTrace]}
      layout={layout}
      useResizeHandler={true}
      style={{ width: "100%", height: "100%" }}
      config={{ responsive: true }}
    />
  );
};

export default TowerPlot;
