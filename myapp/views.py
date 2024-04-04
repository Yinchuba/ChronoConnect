from django.shortcuts import render
from .GraphGenerate import create_graph_from_data, IdentifySignificantNodes, FindKCore, FindCrossTimePathsWithSignificantNodes, FindRelaxedPathsWithSignificantNodes, ExtractFrequentEdges
from .sigPoints import generate_data_files
import os
from .tasks import generate_significant_nodes_image, generate_cross_time_paths_image, generate_relaxed_paths_image, generate_frequent_edges_image

def process_data(request):
    if request.method == 'POST':
        # 处理文件上传
        if 'confirm_file_upload' in request.POST:
            # 使用sigPoints.py生成数据文件
            generate_data_files()

        # 处理重要节点的请求
        if 'confirm_significant_nodes' in request.POST:
            # 从应用目录读取数据文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # 创建图表
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # 确定重要节点
            threshold = 0.5  # 根据需要调整
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # 如果选择了日志输出,将结果传递给模板
            if 'logOutput1' in request.POST:
                context = {'significant_nodes': significant_nodes}
                return render(request, 'index.html', context)

        # 处理子图计算请求
        elif 'confirm_subgraph_calculation' in request.POST:
            # 从应用目录读取数据文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # 创建图表
            graph2 = create_graph_from_data(day2_data)
            
            # 寻找具有重要节点的K-Core
            threshold = 0.5  # 根据需要调整
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            k_core = FindKCore(graph2, significant_nodes)
            
            # 如果选择了日志输出,将结果传递给模板
            if 'logOutput2' in request.POST:
                context = {'k_core_nodes': list(k_core.nodes()), 'k_core_edges': list(k_core.edges())}
                return render(request, 'index.html', context)

        # 处理寻找具有重要节点的跨时间路径请求
        elif 'confirm_cross_time_paths' in request.POST:
            # 从应用目录读取数据文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # 创建图表
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # 确定重要节点
            threshold = 0.5  # 根据需要调整
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # 寻找跨时间路径
            cross_time_paths = FindCrossTimePathsWithSignificantNodes([graph1, graph2], significant_nodes)
            
            # 如果选择了可视化,生成跨时间路径图像
            if 'visualization3' in request.POST:
                generate_cross_time_paths_image.delay([graph1, graph2], cross_time_paths)
                context = {'cross_time_paths_image': '正在生成'}
                return render(request, 'index.html', context)
            
            # 如果选择了日志输出,将结果传递给模板
            if 'logOutput3' in request.POST:
                context = {'cross_time_paths': cross_time_paths}
                return render(request, 'index.html', context)

        # 处理寻找具有重要节点的放松路径请求
        elif 'confirm_relaxed_paths' in request.POST:
            # 从应用目录读取数据文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # 创建图表
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # 确定重要节点
            threshold = 0.5  # 根据需要调整
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # 寻找放松路径
            relaxed_paths = FindRelaxedPathsWithSignificantNodes([graph1, graph2], significant_nodes)
            
            # 如果选择了可视化,生成放松路径图像
            if 'visualization4' in request.POST:
                generate_relaxed_paths_image.delay([graph1, graph2], relaxed_paths)
                context = {'relaxed_paths_image': '正在生成'}
                return render(request, 'index.html', context)
            
            # 如果选择了日志输出,将结果传递给模板
            if 'logOutput4' in request.POST:
                context = {'relaxed_paths': relaxed_paths}
                return render(request, 'index.html', context)

        # 处理路径计算请求
        elif 'confirm_paths_calculation' in request.POST:
            # 从应用目录读取数据文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_dir, 'DataofDay1.txt'), 'r') as file:
                day1_data = file.read()
            with open(os.path.join(current_dir, 'DataofDay2.txt'), 'r') as file:
                day2_data = file.read()
            
            # 创建图表
            graph1 = create_graph_from_data(day1_data)
            graph2 = create_graph_from_data(day2_data)
            
            # 确定重要节点
            threshold = 0.5  # 根据需要调整
            significant_nodes = IdentifySignificantNodes(graph1, graph2, threshold)
            
            # 寻找放松路径
            relaxed_paths = FindRelaxedPathsWithSignificantNodes([graph1, graph2], significant_nodes)
            
            # 提取频繁边
            frequency_threshold = 0.1  # 根据需要调整
            frequent_edges = ExtractFrequentEdges(relaxed_paths, frequency_threshold)
            
            # 如果选择了可视化,生成频繁边图像
            if 'visualization5' in request.POST:
                generate_frequent_edges_image.delay(frequent_edges)
                context = {'frequent_edges_image': '正在生成'}
                return render(request, 'index.html', context)
            
            # 如果选择了日志输出,将结果传递给模板
            if 'logOutput5' in request.POST:
                context = {'frequent_edges': frequent_edges}
                return render(request, 'index.html', context)

    return render(request, 'index.html')
