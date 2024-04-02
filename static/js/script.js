document.addEventListener('DOMContentLoaded', function() {
    initializeConfirmButtonEvents();
    initializeCopyButtonEvents();
    initializeCleanButtonEvents();
    initializeAddFileButtonEvent();
});

function initializeConfirmButtonEvents() {
    document.querySelectorAll('.confirm-btn').forEach(button => {
        button.addEventListener('click', () => {
            const successMessage = button.parentNode.nextElementSibling;
            successMessage.textContent = "Success";
            successMessage.style.display = "inline";

            setTimeout(() => {
                successMessage.style.display = "none";
            }, 3000);

            const dropdownSection = button.closest('.dropdown-section');
            const visualizationCheckbox = dropdownSection.querySelector('input[name^="visualization"]');
            const logOutputCheckbox = dropdownSection.querySelector('input[name^="logOutput"]');

            if (visualizationCheckbox && visualizationCheckbox.checked) {
                const visualizationNumber = visualizationCheckbox.name.slice(-1);
                const visualizationContent = document.querySelector('#visualizationContent');
                visualizationContent.innerHTML = `<img src="${visualizationNumber}.jpg" alt="Visualization ${visualizationNumber}">`;
            }

            if (logOutputCheckbox && logOutputCheckbox.checked) {
                const logOutputNumber = logOutputCheckbox.name.slice(-1);
                const logOutputContent = document.querySelector('#logOutputContent');
                logOutputContent.textContent += `Log Output ${logOutputNumber}\n`;
            }
        });
    });
}

function initializeCopyButtonEvents() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const sectionTitle = btn.closest('.section').querySelector('.section-title').textContent;
            if (sectionTitle.includes('Visualization')) {
                // Assuming visualization content is in an image or similar element.
                alert('Copying images directly is not supported, please download the image instead.');
            } else {
                const logOutput = document.querySelector('#logOutputContent');
                navigator.clipboard.writeText(logOutput.textContent).then(() => {
                    console.log('Text copied to clipboard');
                }).catch(err => {
                    console.error('Could not copy text: ', err);
                });
            }
        });
    });
}

function initializeCleanButtonEvents() {
    document.querySelectorAll('.clean-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const sectionTitle = btn.closest('.section').querySelector('.section-title').textContent;
            if (sectionTitle.includes('Visualization')) {
                document.querySelector('#visualizationContent').innerHTML = '';
            } else {
                document.querySelector('#logOutputContent').textContent = '';
            }
        });
    });
}

function initializeAddFileButtonEvent() {
    document.querySelector('#add-file-btn').addEventListener('click', () => {
        const fileUploadContainer = document.querySelector('.file-upload-container');
        const newFileUploadGroup = document.createElement('div');
        newFileUploadGroup.innerHTML = `
            <input type="file" class="file-upload">
            <p class="upload-feedback">File selected</p>
        `;
        fileUploadContainer.appendChild(newFileUploadGroup);
    });
}

/*
Function 1:
function identifySignificantNodes(graph1, graph2, threshold) {
  const significantNodes = [];
  const nodes = new Set([...graph1.nodes(), ...graph2.nodes()]);

  for (const node of nodes) {
    const weight1 = graph1.edges(`${node}`).reduce((sum, edge) => sum + edge.weight, 0);
    const weight2 = graph2.edges(`${node}`).reduce((sum, edge) => sum + edge.weight, 0);

    if (Math.abs(weight1 - weight2) >= threshold * (weight1 + weight2)) {
      significantNodes.push(node);
    }
  }

  return significantNodes;
}

Function 2:
const nx = require('networkx');

// 创建一个示例图
const G = new nx.Graph();
G.addEdgesFrom([[1, 2], [1, 3], [2, 3], [2, 4], [3, 4], [3, 5], [4, 5], [4, 6], [5, 6]]);

// 计算图的k-core
const k = 3; // 指定k值
const kCore = nx.kCore(G, k);

// 打印k-core的节点和边
console.log(`${k}-core nodes: ${Array.from(kCore.nodes())}`);
console.log(`${k}-core edges: ${Array.from(kCore.edges())}`);

Function 3:
function findCrossTimePathsWithSignificantNodes(graphs, significantNodes) {
  const paths = [];

  for (const graph of graphs) {
    const significantNode = significantNodes.reduce((maxNode, node) => {
      const weightSum = graph.edges(`${node}`).reduce((sum, edge) => sum + edge.weight, 0);
      const maxWeightSum = graph.edges(`${maxNode}`).reduce((sum, edge) => sum + edge.weight, 0);
      return weightSum > maxWeightSum ? node : maxNode;
    });

    const nodePaths = dijkstra(graph, significantNode);

    for (let i = 0; i < graphs.length - 1; i++) {
      const currPaths = nodePaths;
      const nextPaths = dijkstra(graphs[i + 1], significantNodes[i + 1]);

      for (const endNode in currPaths) {
        if (endNode in nextPaths && significantNodes.includes(Number(endNode))) {
          const nextPath = nextPaths[endNode];
          paths.push([...currPaths[endNode], ...nextPath.slice(1)]);
        }
      }
    }
  }

  return paths;
}

Function 4:
function findRelaxedPathsWithSignificantNodes(graphs, significantNodes) {
  const paths = [];

  for (const graph of graphs) {
    const nodePaths = {};
    for (const significantNode of significantNodes) {
      const paths = dijkstra(graph, significantNode);
      for (const node in paths) {
        if (!(node in nodePaths) || paths[node].length < nodePaths[node].length) {
          nodePaths[node] = paths[node];
        }
      }
    }

    for (let i = 0; i < graphs.length - 1; i++) {
      const currPaths = nodePaths;
      const nextPaths = {};
      for (const significantNode of significantNodes) {
        const paths = dijkstra(graphs[i + 1], significantNode);
        for (const node in paths) {
          if (!(node in nextPaths) || paths[node].length < nextPaths[node].length) {
            nextPaths[node] = paths[node];
          }
        }
      }

      for (const [endNode, path] of Object.entries(currPaths)) {
        if (endNode in nextPaths) {
          const nextPath = nextPaths[endNode];
          const newPath = [...path, ...nextPath.slice(1)];
          if (paths.length === 0 || newPath.length < paths[paths.length - 1].length) {
            paths.push(newPath);
          }
        }
      }
    }
  }

  return paths;
}

Function 5:
function extractFrequentEdges(paths, frequencyThreshold) {
  const edgePaths = {};
  const counter = {};

  for (const path of paths) {
    for (let i = 0; i < path.length - 1; i++) {
      const node1 = path[i];
      const node2 = path[i + 1];
      const edge = `${node1},${node2}`;
      counter[edge] = (counter[edge] || 0) + 1;
    }
  }

  for (const edge in counter) {
    if (counter[edge] >= frequencyThreshold) {
      edgePaths[edge] = [];
      for (const path of paths) {
        const nodes = path.join(',');
        if (nodes.includes(edge)) {
          edgePaths[edge].push(path);
        }
      }
    }
  }

  return edgePaths;
}
*/