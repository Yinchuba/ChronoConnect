class Graph {
    constructor() {
        this.nodes = new Set();
        this.edges = new Map();
    }

    addEdge(u, v) {
        if (!this.edges.has(u)) this.edges.set(u, new Set());
        if (!this.edges.has(v)) this.edges.set(v, new Set());

        this.edges.get(u).add(v);
        this.edges.get(v).add(u);

        this.nodes.add(u);
        this.nodes.add(v);
    }

    removeNode(u) {
        if (this.edges.has(u)) {
            for (let v of this.edges.get(u)) {
                this.edges.get(v).delete(u);
                if (this.edges.get(v).size === 0) {
                    this.edges.delete(v);
                    this.nodes.delete(v);
                }
            }
            this.edges.delete(u);
            this.nodes.delete(u);
        }
    }

    getDegree(u) {
        return this.edges.has(u) ? this.edges.get(u).size : 0;
    }

    getNeighbors(u) {
        return this.edges.has(u) ? Array.from(this.edges.get(u)) : [];
    }
}

function calculateKCore() {
    const graph = new Graph();
    graph.addEdge(1, 2);
    graph.addEdge(1, 3);
    graph.addEdge(2, 3);
    graph.addEdge(2, 4);
    graph.addEdge(3, 4);
    graph.addEdge(3, 5);
    graph.addEdge(4, 5);
    graph.addEdge(4, 6);
    graph.addEdge(5, 6);

    const significantNodesInput = document.getElementById('significantNodesInput').value.split(',').map(Number);
    const kValue = parseInt(document.getElementById('kValueInput').value);
    const logOutput = document.getElementById('logOutput');

    // K-Core calculation starts here
    let nodesToRemove = [];
    do {
        nodesToRemove = [];
        for (let node of graph.nodes) {
            if (graph.getDegree(node) < kValue) {
                nodesToRemove.push(node);
            }
        }
        for (let node of nodesToRemove) {
            graph.removeNode(node);
        }
    } while (nodesToRemove.length > 0);

    logOutput.textContent = `Nodes in K-Core: ${Array.from(graph.nodes)}\n`;
}

