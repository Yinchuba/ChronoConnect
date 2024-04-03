from django.shortcuts import render
from .GraphGenerate import create_graph_from_data, IdentifySignificantNodes, FindRelaxedPathsWithSignificantNodes, ExtractFrequentEdges
from .sigPoints import generate_edge_data, modify_edge_data
import networkx as nx
import os
from .tasks import generate_significant_nodes_image, generate_relaxed_paths_image

def process_data(request):
    if request.method == 'POST':
        # Handle file upload
        if 'confirm_file_upload' in request.POST:
            uploaded_file = request.FILES['file_upload']
            file_content = uploaded_file.read().decode('utf-8')
            
            # Generate data files using sigPoints.py
            day1_data = generate_edge_data(10, 20, (1, 10))
            day2_data = modify_edge_data(day1_data, 0.2, (1, 10))
            
            # Save data files to myapp directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'w') as file:
                file.write(day1_data)
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'w') as file:
                file.write(day2_data)

        # Process Significant Nodes request
        if 'confirm_significant_nodes' in request.POST:
            # Read data files from myapp directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # Create graphs
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # Identify significant nodes
            threshold = 0.5  # Adjust as needed
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # Pass results to template if Log Output is selected
            if 'logOutput1' in request.POST:
                context = {'significant_nodes': significant_nodes}
                return render(request, 'index.html', context)

        # Process SubGraph Calculation request
        elif 'confirm_subgraph_calculation' in request.POST:
            # Read data files from myapp directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # Create graph
            graph = nx.parse_edgelist(day1_data.split('\n'), delimiter=' ')
            
            # Calculate k-core
            k = 3  # Adjust as needed
            k_core = nx.k_core(graph, k)
            
            # Pass results to template if Log Output is selected
            if 'logOutput2' in request.POST:
                context = {'k_core_nodes': list(k_core.nodes()), 'k_core_edges': list(k_core.edges())}
                return render(request, 'index.html', context)

        # Process Find Cross Time Paths With Significant Nodes request
        elif 'confirm_cross_time_paths' in request.POST:
            # Read data files from myapp directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # Create graphs
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # Identify significant nodes
            threshold = 0.5  # Adjust as needed
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # Generate significant nodes image asynchronously if Visualization is selected
            if 'visualization3' in request.POST:
                generate_significant_nodes_image.delay(graph1, significant_nodes)
                context = {'significant_nodes_image': 'generating'}
                return render(request, 'index.html', context)
            
            # Pass results to template if Log Output is selected
            if 'logOutput3' in request.POST:
                context = {'significant_nodes_cross_time': significant_nodes}
                return render(request, 'index.html', context)

        # Process Find Relaxed Paths With Significant Nodes request
        elif 'confirm_relaxed_paths' in request.POST:
            # Read data files from myapp directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # Create graphs
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # Identify significant nodes
            threshold = 0.5  # Adjust as needed
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # Find relaxed paths
            relaxed_paths = FindRelaxedPathsWithSignificantNodes([graph1, graph2], significant_nodes)
            
            # Generate relaxed paths image asynchronously if Visualization is selected
            if 'visualization4' in request.POST:
                generate_relaxed_paths_image.delay(graph1, relaxed_paths)
                context = {'relaxed_paths_image': 'generating'}
                return render(request, 'index.html', context)
            
            # Pass results to template if Log Output is selected
            if 'logOutput4' in request.POST:
                context = {'relaxed_paths_nodes': list(set(node for path in relaxed_paths for node in path))}
                return render(request, 'index.html', context)

        # Process Paths Calculation request
        elif 'confirm_paths_calculation' in request.POST:
            # Read data files from myapp directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # Create graphs
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # Extract frequent edges
            frequency_threshold = 0.1  # Adjust as needed
            frequent_edges = ExtractFrequentEdges([graph1, graph2], frequency_threshold)
            
            # Pass results to template if Log Output is selected
            if 'logOutput5' in request.POST:
                context = {'frequent_edges': frequent_edges}
                return render(request, 'index.html', context)

    return render(request, 'index.html')
