from myproject.celery import app  # 从Django项目的Celery配置导入app实例
import matplotlib.pyplot as plt  # 导入matplotlib用于绘图
import networkx as nx  # 导入networkx用于图论和网络分析
import os  # 导入os模块,用于处理文件和目录路径
from .GraphGenerate import visualize_graph, visualize_paths  # 导入自定义的绘图函数

# 定义一个Celery任务,用于生成标注了重要节点的图像
@app.task
def generate_significant_nodes_image(graph, significant_nodes):
    # 调用visualize_graph函数,设置背景色为浅蓝,输出文件名为'significant_nodes.png'
    visualize_graph(graph, "Significant Nodes", 'lightblue', 'significant_nodes.png')

# 定义一个Celery任务,用于生成跨时间路径的图像
@app.task
def generate_cross_time_paths_image(graphs, cross_time_paths):
    # 调用visualize_paths函数,设置背景色为浅绿,输出文件名为'cross_time_paths.png'
    visualize_paths(cross_time_paths, "Cross-Time Paths", 'lightgreen', 'cross_time_paths.png')

# 定义一个Celery任务,用于生成宽松路径的图像
@app.task
def generate_relaxed_paths_image(graphs, relaxed_paths):
    # 调用visualize_paths函数,设置背景色为浅粉,输出文件名为'relaxed_paths.png'
    visualize_paths(relaxed_paths, "Relaxed Paths", 'lightpink', 'relaxed_paths.png')

# 定义一个Celery任务,用于生成频繁边缘的图像
@app.task
def generate_frequent_edges_image(frequent_edges):
    G_frequent = nx.Graph()  # 创建一个新的图用于展示频繁边缘
    for edge, paths in frequent_edges.items():
        G_frequent.add_edge(edge[0], edge[1])  # 将频繁边缘添加到图中
    # 调用visualize_graph函数,设置背景色为浅黄,输出文件名为'frequent_edges.png'
    visualize_graph(G_frequent, "Frequent Edges", 'lightyellow', 'frequent_edges.png')
