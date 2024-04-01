function parseInput(input) {
return input.split('\n').map(line => line.trim()).filter(line => line.length > 0);
}

function extractFrequentEdges() {
const pathsInput = document.getElementById('pathsInput').value;
const thresholdInput = document.getElementById('thresholdInput').value;
const edgePathsOutput = document.getElementById('edgePathsOutput');
const paths = parseInput(pathsInput);
const threshold = parseInt(thresholdInput);

let edgePaths = {};
let counter = {};

for (const path of paths) {
    const nodes = path.split(' -> ');
    for (let i = 0; i < nodes.length - 1; i++) {
        const edge = `${nodes[i]} -> ${nodes[i + 1]}`;
        counter[edge] = (counter[edge] || 0) + 1;
    }
}

for (const edge in counter) {
    if (counter[edge] >= threshold) {
        edgePaths[edge] = [];
        for (const path of paths) {
            if (path.includes(edge)) {
                edgePaths[edge].push(path);
            }
        }
    }
}

edgePathsOutput.textContent = JSON.stringify(edgePaths, null, 2);
}