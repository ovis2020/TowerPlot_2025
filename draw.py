import json
import plotly.graph_objects as go

# Load JSON data
with open("tower_sections.json", "r") as file:
    data = json.load(file)

# Extract coordinates and elements
coordinates = data["coordinates"]
elements = data["elements"]

# Collect all unique nodes from coordinates
all_nodes = set()
for section in coordinates:
    for key, point in section.items():
        if isinstance(point, list):
            all_nodes.add(tuple(point))

# Plot red dots for nodes
fig = go.Figure()

# Plot light blue lines for each element
for section in elements:
    for elem in section["elements"]:
        node_i = elem["node_i"]
        node_j = elem["node_j"]
        fig.add_trace(go.Scatter(
            x=[node_i[0], node_j[0]],
            y=[node_i[1], node_j[1]],
            mode='lines',
            line=dict(color='blue', width=1.5),
            showlegend=False
        ))


x_nodes, y_nodes = zip(*all_nodes)
fig.add_trace(go.Scatter(
    x=x_nodes,
    y=y_nodes,
    mode='markers',
    marker=dict(color='red', size=7),
    name='Nodes',
    showlegend=False
))

# Update layout to match the requirements
fig.update_layout(
        title="Tower Nodes Plot",
        plot_bgcolor='lightgray',
        xaxis=dict(title='X', showgrid=True, dtick=1),
        yaxis=dict(title='Y', showgrid=True, dtick=1, scaleanchor="x", scaleratio=1),
        showlegend=False
    )

fig.show()
