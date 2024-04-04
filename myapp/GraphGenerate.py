import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os

def create_graph_from_data(data):
    """根据给定的数据字符串创建图。数据应该每行包含一个边的信息：源节点 目标节点 权重。"""
    graph = nx.Graph()
    for line in data.split('\n'):
        if line.strip():
            source, target, weight = line.strip().split()
            graph.add_edge(source, target, weight=int(weight))
    return graph

def IdentifySignificantNodes(graph1, graph2, threshold):
    """识别两个图中重要的节点。一个节点被认为是重要的,如果它在两个图中的权重差异大于阈值乘以它们的权重和。"""
    significantNodes = []
    nodes = set(graph1.nodes) | set(graph2.nodes)

    for node in nodes:
        weight1 = sum(int(graph1[node][neighbor]['weight']) for neighbor in graph1[node]) if node in graph1 else 0
        weight2 = sum(int(graph2[node][neighbor]['weight']) for neighbor in graph2[node]) if node in graph2 else 0
        if abs(weight1 - weight2) >= threshold * (weight1 + weight2):
            significantNodes.append(node)

    return significantNodes

def FindKCore(graph, significantNodes):
    """找到含有重要节点的图的k核。首先移除不是重要节点的所有节点,然后计算k核。"""
    if not significantNodes:
        return nx.Graph()
    kCore = graph.copy()
    kCore.remove_nodes_from([node for node in kCore if node not in significantNodes])
    kCore = nx.k_core(kCore)
    return kCore

def FindCrossTimePathsWithSignificantNodes(graphs, significantNodes):
    """在一系列图中找到包含重要节点的跨时间路径。"""
    paths = []

    for graph in graphs:
        significant_nodes_in_graph = [node for node in significantNodes if node in graph]
        if significant_nodes_in_graph:
            significant_node = max(significant_nodes_in_graph, key=lambda node: sum(int(graph[node][neighbor]['weight']) for neighbor in graph[node]))
            nodePaths = nx.single_source_dijkstra_path(graph, significant_node)

            for i in range(len(graphs) - 1):
                currPaths = nodePaths
                if significant_node in graphs[i+1]:
                    nextPaths = nx.single_source_dijkstra_path(graphs[i+1], significant_node)
                    for endNode in currPaths:
                        if endNode in nextPaths and endNode in significantNodes:
                            nextPath = nextPaths[endNode]
                            paths.append(currPaths[endNode] + nextPath[1:])
    return paths

def FindRelaxedPathsWithSignificantNodes(graphs, significantNodes):
    """在一系列图中找到包含重要节点的放松路径。不同于跨时间路径,放松路径不要求路径在每个图中都是最短的。"""
    paths = []

    for graph in graphs:
        nodePaths = {}
        for node in significantNodes:
            if node in graph:
                nodePaths.update(nx.single_source_dijkstra_path(graph, node))

        for i in range(len(graphs) - 1):
            currPaths = nodePaths
            nextPaths = {}
            for node in significantNodes:
                if node in graphs[i+1]:
                    nextPaths.update(nx.single_source_dijkstra_path(graphs[i+1], node))
            for endNode, path in currPaths.items():
                if endNode in nextPaths:
                    nextPath = nextPaths[endNode]
                    newPath = path + nextPath[1:]
                    if not paths or len(newPath) < len(paths[-1]):
                        paths.append(newPath)

    return paths

def ExtractFrequentEdges(paths, frequency_threshold=0.1):
    """从一系列路径中提取出现频率超过阈值的边。"""
    edgePaths = {}
    counter = Counter()

    for path in paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            counter[edge] += 1

    for edge, count in counter.items():
        if count >= frequency_threshold * len(paths):
            edgePaths[edge] = []
            for path in paths:
                if edge[0] in path and edge[1] in path:
                    edgePaths[edge].append(path)

    return edgePaths

def visualize_graph(graph, title, node_color, filename):
    """使用matplotlib可视化一个图,将结果保存为文件。"""
    if not graph.edges():
        print(f"{title} is empty. Skipping visualization.")
    else:
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(graph)
        nx.draw_networkx(graph, pos, node_size=500, node_color=node_color, font_size=12, font_weight='bold', edge_color='gray', width=1.5, with_labels=True)
        labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
        os.makedirs(static_dir, exist_ok=True)
        plt.savefig(os.path.join(static_dir, filename), dpi=300)
        plt.close()

def visualize_paths(paths, title, node_color, filename):
    """使用matplotlib可视化一系列路径,将结果保存为文件。"""
    if not paths:
        print(f"No {title} found. Skipping visualization.")
    else:
        plt.figure(figsize=(12, 10))
        G_visual = nx.Graph()
        colors = cm.rainbow(np.linspace(0, 1, len(paths)))
        for i, path in enumerate(paths):
            for j in range(len(path) - 1):
                G_visual.add_edge(path[j], path[j+1], color=colors[i])
        pos = nx.spring_layout(G_visual)
        edges = G_visual.edges()
        edge_colors = [G_visual[u][v]['color'] for u,v in edges]
        nx.draw_networkx(G_visual, pos, node_size=500, node_color=node_color, font_size=12, font_weight='bold', edge_color=edge_colors, width=1.5, with_labels=True)
        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
        os.makedirs(static_dir, exist_ok=True)
        plt.savefig(os.path.join(static_dir, filename), dpi=300)
        plt.close()
