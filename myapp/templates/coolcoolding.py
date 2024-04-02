import networkx as nx
from collections import Counter

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

def FindKCore(graph, significantNodes):
    if not significantNodes:
        return nx.Graph()
    kCore = graph.copy()
    kCore.remove_nodes_from([node for node in kCore if node not in significantNodes])
    kCore = nx.k_core(kCore)
    return kCore

def FindCrossTimePathsWithSignificantNodes(graphs, significantNodes):
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

day1_data = """
D S 6
N P 1
N A 4
G K 6
I L 2
H R 1
H T 4
N F 2
M O 6
L D 6
P C 3
I N 4
A L 3
G L 10
S T 2
M K 7
A I 6
G H 4
G N 2
D L 3
I G 1
N R 3
G P 7
D N 9
G B 1
L J 3
B D 3
D I 5
P M 2
K M 6
I J 2
D A 10
R O 9
J S 8
S M 10
A J 10
A H 4
T K 3
R I 6
L A 7
C I 3
Q L 3
N D 6
I C 8
H O 6
P S 6
C E 8
D Q 1
H I 3
E F 3
F D 3
B J 10
A E 5
T L 3
G R 5
S O 5
G C 5
Q A 1
O E 1
T N 10
R L 5
D P 5
T I 1
B E 7
R H 9
N L 6
O F 1
T B 9
T E 4
L C 8
O G 5
B F 3
T A 7
J N 10
H J 6
B G 10
I T 1
K Q 5
E C 3
C R 10
M A 8
R E 6
H N 3
A R 5
J B 8
R A 6
A C 8
S L 1
R F 9
F P 2
J F 5
O R 9
K A 8
N Q 7
N J 1
K F 10
T C 4
S A 9
F Q 3
G O 6
"""

day2_data = """
D S 6
N P 1
N A 30
G K 22
I L 24
H R 1
H T 8
N F 9
M O 30
L D 3
P C 28
I N 1
A L 7
G L 25
S T 29
M K 16
A I 17
G H 22
G N 3
D L 8
I G 13
N R 5
G P 14
D N 9
G B 8
L J 3
B D 7
D I 13
P M 23
K M 11
I J 18
D A 29
R O 24
J S 3
S M 16
A J 16
A H 2
T K 3
R I 27
L A 9
C I 3
Q L 14
N D 9
I C 2
H O 6
P S 8
C E 8
D Q 25
H I 7
E F 28
F D 25
B J 10
A E 16
T L 12
G R 15
S O 23
G C 9
Q A 15
O E 26
T N 2
R L 10
D P 5
T I 18
B E 28
R H 14
N L 6
O F 14
T B 25
T E 19
L C 23
O G 5
B F 1
T A 10
J N 10
H J 1
B G 4
I T 19
K Q 5
E C 22
C R 23
M A 13
R E 4
H N 19
A R 5
J B 12
R A 18
A C 4
S L 12
R F 18
F P 15
J F 5
O R 14
K A 8
N Q 12
N J 8
K F 4
T C 10
S A 27
F Q 28
G O 1
"""

graph1 = create_graph_from_data(day1_data)
graph2 = create_graph_from_data(day2_data)

threshold = 0.5
significantNodes = IdentifySignificantNodes(graph1, graph2, threshold)
print("Significant Nodes:", significantNodes)

kCore = FindKCore(graph2, significantNodes)
print("K-Core:")
print(list(kCore.edges(data=True)))

graphs = [graph1, graph2]
crossTimePaths = FindCrossTimePathsWithSignificantNodes(graphs, significantNodes)
print("Cross-Time Paths with Significant Nodes:")
for path in crossTimePaths:
    print(path)

relaxedPaths = FindRelaxedPathsWithSignificantNodes(graphs, significantNodes)
print("Relaxed Paths with Significant Nodes:")
for path in relaxedPaths:
    print(path)

frequentEdges = ExtractFrequentEdges(relaxedPaths)
print("Frequent Edges:")
for edge, paths in frequentEdges.items():
    print(edge)
    for path in paths:
        print("  ", path)