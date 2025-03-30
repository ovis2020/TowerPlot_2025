import json
import plotly.graph_objects as go

# Load JSON data
with open("tower_sections.json", "r") as file:
    data = json.load(file)

coordinates = data["coordinates"]
elements = data["elements"]

# Compute base width and center for x-range (adjust to 2x base width)
base_width = coordinates[0]["b"][0] - coordinates[0]["a"][0]
x_center = (coordinates[0]["b"][0] + coordinates[0]["a"][0]) / 2
x_range = [x_center - base_width, x_center + base_width * 2]

# Collect all unique nodes (for red dots only, no labels)
all_nodes = set()
for section in coordinates:
    for key, point in section.items():
        if isinstance(point, list):
            all_nodes.add(tuple(point))

# Create figure
fig = go.Figure()

# Alternate colors for sections: red, white, red, white...
section_colors = ['red', 'white']
for i, section in enumerate(elements):
    color = section_colors[i % 2]
    for elem in section["elements"]:
        x_vals = [elem["node_i"][0], elem["node_j"][0]]
        y_vals = [elem["node_i"][1], elem["node_j"][1]]
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            line=dict(color=color, width=2),
            showlegend=False
        ))

# Plot red dots for each unique node
x_nodes, y_nodes = zip(*all_nodes)
fig.add_trace(go.Scatter(
    x=x_nodes,
    y=y_nodes,
    mode='markers',
    marker=dict(color='red', size=6),
    showlegend=False
))

# Final layout style
fig.update_layout(
    xaxis=dict(showgrid=True, gridcolor='#FFCC99', dtick=1, range=x_range),
    yaxis=dict(showgrid=True, gridcolor='#FFCC99', dtick=1, scaleanchor="x", scaleratio=1),
    plot_bgcolor='#2a2a2a',
    paper_bgcolor='#2a2a2a',
    margin=dict(l=10, r=10, t=10, b=10),
    title="Tower Structure by Section (Alternating Red/White)"
)

fig.show()
