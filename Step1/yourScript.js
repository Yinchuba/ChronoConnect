function processCSVFiles() {
  const input1 = document.getElementById('csvFileInput1');
  const input2 = document.getElementById('csvFileInput2');
  const outputElement = document.getElementById('output');

  if (input1.files.length > 0 && input2.files.length > 0) {
    outputElement.textContent = 'Processing...'; // 提示用户处理中

    const file1 = input1.files[0];
    const file2 = input2.files[0];

    Promise.all([fileToGraph(file1), fileToGraph(file2)]).then(([graph1, graph2]) => {
      const significantNodes = identifySignificantNodes(graph1, graph2, 0.1); // 假设threshold是0.1
      outputElement.textContent = 'Significant Nodes: ' + significantNodes.join(', ');
    }).catch(error => {
      outputElement.textContent = 'Error processing files: ' + error;
    });
  } else {
    outputElement.textContent = "Please select both files before processing.";
  }
}

function fileToGraph(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = function(e) {
      const text = e.target.result;
      const graph = parseCSVToGraph(text);
      resolve(graph);
    };
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

function parseCSVToGraph(csvText) {
  const lines = csvText.trim().split('\n').slice(1); // 去掉标题行
  const nodes = new Set();
  const edges = {};

  lines.forEach(line => {
    const [id, outNode, inNode, value] = line.split(',');
    nodes.add(outNode);
    nodes.add(inNode);

    if (!edges[outNode]) edges[outNode] = [];
    if (!edges[inNode]) edges[inNode] = []; // 确保每个节点都在edges对象中

    edges[outNode].push({ node: inNode, weight: parseFloat(value) });
  });

  return {
    nodes: () => Array.from(nodes),
    edges: (node) => edges[node] || []
  };
}

function identifySignificantNodes(graph1, graph2, threshold) {
  const significantNodes = [];
  const nodes = new Set([...graph1.nodes(), ...graph2.nodes()]);

  for (const node of nodes) {
    const weight1 = graph1.edges(node).reduce((sum, edge) => sum + edge.weight, 0);
    const weight2 = graph2.edges(node).reduce((sum, edge) => sum + edge.weight, 0);

    if (Math.abs(weight1 - weight2) >= threshold * (weight1 + weight2)) {
      significantNodes.push(node);
    }
  }

  return significantNodes;
}
