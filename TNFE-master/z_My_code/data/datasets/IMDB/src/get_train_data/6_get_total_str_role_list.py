# 计算整个网络下，每个节点的拓扑势，以列表形式保存

import math
import networkx as nx
import pickle
import numpy as np

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\imdb_graph.pkl','rb') as fr:
    G = pickle.load(fr)

# 计算某个节点在某个网络中的结构角色(结构拓扑势)
impact = 1.3405
def compute_structural_role(G, node_i):
    structural_role_i = 0

    # 计算当前节点与网络中所有可到达节点的最短路径长度字典,只不过边的权重为1
    shortest_path_length_dict = nx.single_source_shortest_path_length(G, node_i)
    # 计算当前节点与网络中所有可到达节点的最短路径长度字典
    shortest_path_length_weighted_dict = nx.single_source_dijkstra_path_length(G, node_i, weight="w")

    for node_j in nx.nodes(G):
        print(node_j)
        if (node_j != node_i):
            # 获得网络G中其他节点的度数
            mj = G.in_degree(node_j) + G.out_degree(node_j)
            # 获得网络中节点间最短路径长度
            if(node_j not in shortest_path_length_dict.keys()):
                dk = 10
            else:
                dk = shortest_path_length_dict[node_j]
            # wk = 0
            # for i in range(len(shortest_path_list)-1):
            #     wk = wk + G.get_edge_data(shortest_path_list[i], shortest_path_list[i+1])[list(G.get_edge_data(shortest_path_list[i], shortest_path_list[i+1]).keys())[0]]['w']
            if (node_j not in shortest_path_length_weighted_dict.keys()):
                wk = 10
            else:
                wk = shortest_path_length_weighted_dict[node_j]  # 最短加权路径长度(边的权重之和)
            wij = dk / wk

            # 利用高斯势函数定义节点i的结构角色重要性
            structural_role_i = structural_role_i + mj*math.exp(-math.pow(wij/impact,2))
    return structural_role_i / nx.number_of_nodes(G)

# 对列表中的元素去重，并按照原先顺序返回
def remove_same(orgList):
    formatList = []
    for id in orgList:
        if id not in formatList:
            formatList.append(id)
    return formatList

# 计算所有节点的总拓扑势，放在列表中
total_str_role_list = []
idx = 0
node_list = []    # 按照het_neigh_train.txt文件中的节点顺序，来计算总拓扑势
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\generated_data\het_neigh_train.txt','rb') as edge_file:
    neigh_lines = edge_file.readlines()
    for line in neigh_lines:
        neigh_list = line.decode().split()
        node_list.append(neigh_list[0])    # 将het_neigh_train.txt文件中每行的第一个节点保存在列表中
edge_file.close()

for node in node_list:
    # 计算拓扑势
    total_str_role = compute_structural_role(G, node)
    total_str_role_list.append(total_str_role)
    print("已添加到列表，计算完成了节点", idx)
    idx = idx + 1
print(total_str_role_list)
np.save(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\train_data\total_str_role_list.npy', total_str_role_list)