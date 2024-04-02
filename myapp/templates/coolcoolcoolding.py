import matplotlib.pyplot as plt
import networkx as nx
import ast
from matplotlib import cm
import numpy as np


with open('results.txt', 'r', encoding='latin-1') as file:
    lines = file.readlines()


significantNodes = ast.literal_eval(lines[0].split(': ')[1].strip())


kCore_edges = []
i = 3
while lines[i].strip() != "Cross-Time Paths with Significant Nodes:":
    if lines[i].strip():
        kCore_edges.append(ast.literal_eval(lines[i].strip()))
    i += 1


kCore = nx.Graph()
for edge in kCore_edges:
    kCore.add_edge(edge[0], edge[1], weight=edge[2]['weight'])


crossTimePaths = []
i += 1
while lines[i].strip() != "Relaxed Paths with Significant Nodes:":
    if lines[i].strip():
        crossTimePaths.append(ast.literal_eval(lines[i].strip()))
    i += 1


relaxedPaths = []
i += 1
while lines[i].strip() != "Frequent Edges:":
    if lines[i].strip():
        relaxedPaths.append(ast.literal_eval(lines[i].strip()))
    i += 1


frequentEdges = {}
i += 1
while i < len(lines):
    if lines[i].strip():
        edge = ast.literal_eval(lines[i].strip())
        frequentEdges[edge] = []
        i += 1
        while i < len(lines) and lines[i].startswith("  "):
            frequentEdges[edge].append(ast.literal_eval(lines[i].strip()))
            i += 1
    else:
        i += 1

if not kCore.edges():
    print("K-Core is empty. Skipping visualization.")
else:
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(kCore)
    nx.draw_networkx(kCore, pos, node_size=500, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray', width=1.5, with_labels=True)
    labels = nx.get_edge_attributes(kCore, 'weight')
    nx.draw_networkx_edge_labels(kCore, pos, edge_labels=labels)
    plt.title("K-Core")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('k_core.png', dpi=300)
    plt.close()


if not crossTimePaths:
    print("No Cross-Time Paths found. Skipping visualization.")
else:
    plt.figure(figsize=(12, 10))
    G_visual = nx.Graph()
    colors = cm.rainbow(np.linspace(0, 1, len(crossTimePaths)))
    for i, path in enumerate(crossTimePaths):
        for j in range(len(path) - 1):
            G_visual.add_edge(path[j], path[j+1], color=colors[i])
    pos = nx.spring_layout(G_visual)
    edges = G_visual.edges()
    edge_colors = [G_visual[u][v]['color'] for u,v in edges]
    nx.draw_networkx(G_visual, pos, node_size=500, node_color='lightgreen', font_size=12, font_weight='bold', edge_color=edge_colors, width=1.5, with_labels=True)
    plt.title("Cross-Time Paths")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('cross_time_paths.png', dpi=300)
    plt.close()


if not relaxedPaths:
    print("No Relaxed Paths found. Skipping visualization.")
else:
    plt.figure(figsize=(12, 10))
    G_visual = nx.Graph()
    colors = cm.rainbow(np.linspace(0, 1, len(relaxedPaths)))
    for i, path in enumerate(relaxedPaths):
        for j in range(len(path) - 1):
            G_visual.add_edge(path[j], path[j+1], color=colors[i])
    pos = nx.spring_layout(G_visual)
    edges = G_visual.edges()
    edge_colors = [G_visual[u][v]['color'] for u,v in edges]
    nx.draw_networkx(G_visual, pos, node_size=500, node_color='lightpink', font_size=12, font_weight='bold', edge_color=edge_colors, width=1.5, with_labels=True)
    plt.title("Relaxed Paths")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('relaxed_paths.png', dpi=300)
    plt.close()


plt.figure(figsize=(8, 6))
G_visual = nx.Graph()
for edge, paths in frequentEdges.items():
    G_visual.add_edge(edge[0], edge[1])
pos = nx.spring_layout(G_visual)
nx.draw_networkx(G_visual, pos, node_size=500, node_color='lightyellow', font_size=12, font_weight='bold', edge_color='gray', width=1.5, with_labels=True)
plt.title("Frequent Edges")
plt.axis('off')
plt.tight_layout()
plt.savefig('frequent_edges.png', dpi=300)
plt.close()