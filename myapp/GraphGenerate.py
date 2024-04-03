import networkx as nx

def create_graph_from_data(data):
    graph = nx.Graph()
    for line in data.split('\n'):
        if line.strip():
            source, target, weight = line.strip().split()
            graph.add_edge(source, target, weight=int(weight))
    return graph

def IdentifySignificantNodes(graph1, graph2, threshold):
    significantNodes = []
    nodes = set(graph1.nodes) | set(graph2.nodes)

    for node in nodes:
        weight1 = sum(int(graph1[node][neighbor]['weight']) for neighbor in graph1[node]) if node in graph1 else 0
        weight2 = sum(int(graph2[node][neighbor]['weight']) for neighbor in graph2[node]) if node in graph2 else 0
        if abs(weight1 - weight2) >= threshold * (weight1 + weight2):
            significantNodes.append(node)

    return significantNodes

def FindRelaxedPathsWithSignificantNodes(graphs, significantNodes):
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
    edgePaths = {}
    counter = Counter()

    for path in paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            counter[edge] += 1

    for edge, count in counter.items():
        if count >= frequency_threshold:
            edgePaths[edge] = []
            for path in paths:
                if edge[0] in path and edge[1] in path:
                    edgePaths[edge].append(path)

    return edgePaths