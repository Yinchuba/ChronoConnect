function parseInput(input) {
return input.split('\n').map(line => line.trim()).filter(line => line.length > 0);
}

function dijkstra(graph, source) {
return {};
}

function findRelaxedPaths() {
const graphsInput = document.getElementById('graphsInput').value;
const significantNodesInput = document.getElementById('significantNodesInput').value;
const pathsOutput = document.getElementById('pathsOutput');
const graphs = parseInput(graphsInput);
const significantNodes = parseInput(significantNodesInput);

let paths = [];

for (let i = 0; i < graphs.length - 1; i++) {
    const currGraph = graphs[i];
    const nextGraph = graphs[i + 1];
    const nodePaths = dijkstra(currGraph, significantNodes);

    for (const [endNode, path] of Object.entries(nodePaths)) {
        if (endNode in dijkstra(nextGraph, significantNodes)) {
            const nextPath = dijkstra(nextGraph, significantNodes)[endNode];
            const newPath = path.concat(nextPath.slice(1));

            if (paths.length === 0 || newPath.length < paths[paths.length - 1].length) {
                paths.push(newPath);
            }
        }
    }
}

pathsOutput.textContent = `Found paths:\n${paths.map(path => path.join(' -> ')).join('\n')}`;