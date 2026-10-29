import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon

def get_hex_center(q, r, radius=1.0):
    x = radius * np.sqrt(3) * (q + r / 2.0)
    y = radius * 1.5 * r
    return x, y

def create_three_clusters(radius=1.0):
    cluster_offsets = [
        (0, 0),      # Cluster 1 (Bottom Left)
        (3, -1),     # Cluster 2 (Bottom Right)
        (1, 3)       # Cluster 3 (Top Middle)
    ]
    local_cells = [
        (0, 0, 'A'),
        (1, 0, 'B'),
        (0, 1, 'C'),
        (1, 1, 'D')
    ]
    all_cells = []
    cell_id = 1
    for cluster_idx, (cq, cr) in enumerate(cluster_offsets):
        for dq, dr, group in local_cells:
            q = cq + dq
            r = cr + dr
            x, y = get_hex_center(q, r, radius)
            all_cells.append({
                'id': cell_id,
                'cluster': cluster_idx + 1,
                'group': group,
                'x': x,
                'y': y
            })
            cell_id += 1
    return all_cells

def plot_tight_clusters(cells, title):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    group_colors = {
        'A': '#FF9999',
        'B': '#66B2FF',
        'C': '#99FF99',
        'D': '#FFCC99'
    }
    for cell in cells:
        facecolor = group_colors[cell['group']]
        hex_cell = RegularPolygon(
            (cell['x'], cell['y']),
            numVertices=6,
            radius=1.0,
            orientation=0,
            facecolor=facecolor,
            edgecolor='black',
            linewidth=1.5,
            alpha=0.85
        )
        ax.add_patch(hex_cell)
        ax.text(cell['x'], cell['y'] + 0.15, f"Cell {cell['id']}",
                ha='center', va='center', weight='bold', fontsize=8)
        ax.text(cell['x'], cell['y'] - 0.05, f"Cluster {cell['cluster']}",
                ha='center', va='center', fontsize=7)
        ax.text(cell['x'], cell['y'] - 0.25, f"Group: {cell['group']}",
                ha='center', va='center', weight='bold', fontsize=8)
    ax.autoscale_view()
    plt.title(title, fontsize=14, weight='bold')
    plt.xlabel("X Distance")
    plt.ylabel("Y Distance")
    plt.grid(False)
    plt.show()

cells_data = create_three_clusters(radius=1.0)
plot_tight_clusters(
    cells_data,
    title="3 Contiguous Clusters (N=4, Groups A-D) with Reuse Distance"
)

incorrect_cells_data = create_three_clusters(radius=1.0)
incorrect_cells_data[6]['group'] = 'D'
incorrect_cells_data[7]['group'] = 'C'

def plot_tight_clusters_cci(cells, title, cci_cell_ids=[]):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    group_colors = {
        'A': '#FF9999',
        'B': '#66B2FF',
        'C': '#99FF99',
        'D': '#FFCC99'
    }
    for cell in cells:
        facecolor = group_colors[cell['group']]
        edgecolor = 'black'
        linewidth = 1.5
        if cell['id'] in cci_cell_ids:
            edgecolor = 'red'
            linewidth = 3.5
        hex_cell = RegularPolygon(
            (cell['x'], cell['y']),
            numVertices=6,
            radius=1.0,
            orientation=0,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linewidth=linewidth,
            alpha=0.85
        )
        ax.add_patch(hex_cell)
        ax.text(cell['x'], cell['y'] + 0.15, f"Cell {cell['id']}",
                ha='center', va='center', weight='bold', fontsize=8)
        ax.text(cell['x'], cell['y'] - 0.05, f"Cluster {cell['cluster']}",
                ha='center', va='center', fontsize=7)
        ax.text(cell['x'], cell['y'] - 0.25, f"Group: {cell['group']}",
                ha='center', va='center', weight='bold', fontsize=8)
    ax.autoscale_view()
    plt.title(title, fontsize=14, weight='bold')
    plt.xlabel("X Distance")
    plt.ylabel("Y Distance")
    plt.grid(False)
    plt.show()

plot_tight_clusters_cci(
    incorrect_cells_data,
    title="Incorrect Allocation: Interchanged Group C & D in Cluster 2 Causing CCI",
    cci_cell_ids=[4, 7]
)

