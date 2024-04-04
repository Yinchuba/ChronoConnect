from myproject.celery import app
import matplotlib.pyplot as plt
import networkx as nx
import os

@app.task
def generate_significant_nodes_image(graph, significant_nodes):
    plt.figure()
    nx.draw(graph, with_labels=True)
    nx.draw_networkx_nodes(graph, nodelist=significant_nodes, node_color='r')
    
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    os.makedirs(static_dir, exist_ok=True)
    plt.savefig(os.path.join(static_dir, 'significant_nodes.png'), format='png')
    plt.close()

@app.task
def generate_relaxed_paths_image(graph, relaxed_paths):
    plt.figure()
    for path in relaxed_paths:
        edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_nodes(graph, nodelist=path, node_color='r')
        nx.draw_networkx_edges(graph, edgelist=edges, edge_color='r', width=2)
    nx.draw(graph, with_labels=True)
    
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    os.makedirs(static_dir, exist_ok=True)
    plt.savefig(os.path.join(static_dir, 'relaxed_paths.png'), format='png')
    plt.close()
