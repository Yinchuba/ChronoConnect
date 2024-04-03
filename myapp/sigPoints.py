import random
import string

def generate_edge_data(num_nodes, num_edges, weight_range):
    nodes = list(string.ascii_uppercase[:num_nodes])
    edges = set()
    while len(edges) < num_edges:
        source = random.choice(nodes)
        target = random.choice(nodes)
        if source != target:
            edges.add((source, target))
    edge_data = []
    for edge in edges:
        weight = random.randint(*weight_range)
        edge_data.append(f"{edge[0]} {edge[1]} {weight}")
    return "\n".join(edge_data)

def modify_edge_data(edge_data, change_ratio, weight_range):
    edges = edge_data.split("\n")
    new_edges = []
    for edge in edges:
        if random.random() < change_ratio:
            source, target, _ = edge.split()
            new_weight = random.randint(*weight_range)
            new_edges.append(f"{source} {target} {new_weight}")
        else:
            new_edges.append(edge)
    return "\n".join(new_edges)