import networkx as nx

# 指定源节点和目标节点
source_node = '1'
target_node = '3'

# 使用 shortest_path_length 计算最短路径长度
try:
    shortest_distance = nx.shortest_path_length(G, source=source_node, target=target_node)
    print(f"从节点 {source_node} 到节点 {target_node} 的最短路径距离是: {shortest_distance}")
except nx.NetworkXNoPath:
    print(f"从节点 {source_node} 到节点 {target_node} 不存在路径")
