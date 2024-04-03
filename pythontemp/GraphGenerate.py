{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Application</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div class="container">
        <div class="section" id="left-section">
            <div class="section-header">
                <p class="section-title">Algorithm</p>
            </div>
            <form method="post" enctype="multipart/form-data">
                {% csrf_token %}
                <div class="file-upload-container">
                    <div class="file-upload-group">
                        <input type="file" name="file_upload" class="file-upload">
                        <p class="upload-feedback"></p>
                    </div>
                    <button type="submit" name="confirm_file_upload" class="confirm-btn">Confirm</button>
                </div>
                <div class="dropdown-section">
                    <p>Significant Nodes</p>
                    <div class="dropdown-container">
                        <select name="significant_nodes">
                            <option value="default">Default</option>
                            <option value="maximum">Maximum</option>
                            <option value="minimum">Minimum</option>
                            <option value="average">Average</option>
                        </select>
                        <button type="submit" name="confirm_significant_nodes" class="confirm-btn">Confirm</button>
                    </div>
                    <p class="success-message"></p><br><br>
                    <label class="checkbox-label"><input type="checkbox" name="logOutput1">Log Output</label>
                </div>
                <div class="dropdown-section">
                    <p>SubGraph Calculation</p>
                    <div class="dropdown-container">
                        <select name="subgraph_calculation">
                            <option value="findKCore">Find KCore</option>
                            <option value="louvainMethod">Louvain Method</option>
                            <option value="girvanNewman">Girvan-Newman Algorithm</option>
                            <option value="corenessCentrality">Coreness Centrality</option>
                        </select>
                        <button type="submit" name="confirm_subgraph_calculation" class="confirm-btn">Confirm</button>
                    </div>
                    <p class="success-message"></p><br><br>
                    <label class="checkbox-label"><input type="checkbox" name="logOutput2">Log Output</label>
                </div>
                <div class="dropdown-section">
                    <p>Find Cross Time Paths With Significant Nodes</p>
                    <div class="dropdown-container">
                        <select name="cross_time_paths">
                            <option value="default">Default</option>
                            <option value="parallel">Parallel</option>
                            <option value="divide">Divide</option>
                            <option value="parallelDivide">Parallel & Divide</option>
                        </select>
                        <button type="submit" name="confirm_cross_time_paths" class="confirm-btn">Confirm</button>
                    </div>
                    <p class="success-message"></p><br>
                    <label class="checkbox-label"><input type="checkbox" name="visualization3">Visualization</label><br>
                    <label class="checkbox-label"><input type="checkbox" name="logOutput3">Log Output</label>
                </div>
                <div class="dropdown-section">
                    <p>Find Relaxed Paths With Significant Nodes</p>
                    <div class="dropdown-container">
                        <select name="relaxed_paths">
                            <option value="default">Default</option>
                            <option value="parallel">Parallel</option>
                            <option value="divide">Divide</option>
                            <option value="parallelDivide">Parallel & Divide</option>
                        </select>
                        <button type="submit" name="confirm_relaxed_paths" class="confirm-btn">Confirm</button>
                    </div>
                    <p class="success-message"></p><br>
                    <label class="checkbox-label"><input type="checkbox" name="visualization4">Visualization</label><br>
                    <label class="checkbox-label"><input type="checkbox" name="logOutput4">Log Output</label>
                </div>
                <div class="dropdown-section">
                    <p>Paths Calculation</p>
                    <div class="dropdown-container">
                        <select name="paths_calculation">
                            <option value="extractFrequentEdges">Extract Frequent Edges</option>
                            <option value="aprioriAlgorithm">Apriori Algorithm</option>
                            <option value="eclatAlgorithm">Eclat Algorithm</option>
                            <option value="fpGrowthAlgorithm">FP-Growth Algorithm</option>
                        </select>
                        <button type="submit" name="confirm_paths_calculation" class="confirm-btn">Confirm</button>
                    </div>
                    <p class="success-message"></p><br>
                    <label class="checkbox-label"><input type="checkbox" name="visualization5">Visualization</label><br>
                    <label class="checkbox-label"><input type="checkbox" name="logOutput5">Log Output</label>
                </div>
            </form>
        </div>
        <div class="section" id="middle-section">
            <div class="section-header">
                <p class="section-title">Visualization</p>
            </div>
            <div class="content-container">
                <div id="visualizationContent">
                    {% if significant_nodes_image %}
                        <img src="{% static significant_nodes_image %}" alt="Significant Nodes">
                    {% endif %}
                    {% if relaxed_paths_image %}
                        <img src="{% static relaxed_paths_image %}" alt="Relaxed Paths">
                    {% endif %}
                </div>
                <div class="button-group">
                    <button class="small-btn copy-btn">Copy</button>
                    <button class="small-btn clean-btn">Clean</button>
                </div>
            </div>
        </div>
        <div class="section" id="right-section">
            <div class="section-header">
                <p class="section-title">Log Output</p>
            </div>
            <div class="content-container">
                <div id="logOutputContent">
                    {% if significant_nodes %}
                        <h4>Significant Nodes:</h4>
                        <pre>{{ significant_nodes }}</pre>
                    {% endif %}
                    {% if k_core_nodes %}
                        <h4>K-Core Nodes:</h4>
                        <pre>{{ k_core_nodes }}</pre>
                    {% endif %}
                    {% if k_core_edges %}
                        <h4>K-Core Edges:</h4>
                        <pre>{{ k_core_edges }}</pre>
                    {% endif %}
                    {% if significant_nodes_cross_time %}
                        <h4>Cross Time Paths Significant Nodes:</h4>
                        <pre>{{ significant_nodes_cross_time }}</pre>
                    {% endif %}
                    {% if relaxed_paths_nodes %}
                        <h4>Relaxed Paths Nodes:</h4>
                        <pre>{{ relaxed_paths_nodes }}</pre>
                    {% endif %}
                    {% if frequent_edges %}
                        <h4>Frequent Edges:</h4>
                        <pre>{{ frequent_edges }}</pre>
                    {% endif %}
                </div>
                <div class="button-group">
                    <button class="small-btn copy-btn">Copy</button>
                    <button class="small-btn clean-btn">Clean</button>
                </div>
            </div>
        </div>
    </div>
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>