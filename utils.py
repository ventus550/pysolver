import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from itertools import product


def plot_graph(flow, capacity, seed=123):
    # Create a directed graph
    G = nx.DiGraph()
    n = len(flow)

    # Add edges with attributes flow and capacity
    for v, u in product(range(n), repeat=2):
        if capacity[v, u] > 0:  # If there's a capacity, add the edge
            G.add_edge(
                v or "s",
                u if u != n - 1 else "t",
                flow=flow[v, u],
                capacity=capacity[v, u],
            )

    # Prepare edge colors and widths based on flow/capacity
    lightblue = np.array([173, 216, 230]) / 255
    lightgrey = np.array([210, 210, 210]) / 255
    edge_colors = []
    for u, v, data in G.edges(data=True):
        flow = data["flow"]
        capacity = data["capacity"]
        if flow > capacity:
            edge_colors.append("red")
        else:
            ratio = float(flow) / float(capacity)
            edge_colors.append(ratio * lightblue + (1 - ratio) * lightgrey)

    for layer, nodes in enumerate(nx.topological_generations(G)):
        # `multipartite_layout` expects the layer as a node attribute, so add the
        # numeric layer value as a node attribute
        for node in nodes:
            G.nodes[node]["layer"] = layer

    # Draw the graph
    # pos = nx.spring_layout(G, seed=seed, k=10/np.sqrt(n))  # positions for all nodes
    pos = nx.multipartite_layout(G, subset_key="layer")  # positions for all nodes

    # Draw nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_family="sans-serif")

    # Draw edges with custom styles
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=True)

    # Add edge labels (optional)
    edge_labels = {
        (u, v): f"{data['flow']:.1f}/{data['capacity']:.1f}"
        for u, v, data in G.edges(data=True)
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    # Show plot
    plt.axis("off")
    plt.tight_layout()
    plt.show()