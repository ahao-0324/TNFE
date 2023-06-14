# 结构拓扑势的计算，以及利用pso得到局部网络的采样

import math
import z_My_code.data.datasets.ACM.src.get_train_data.pso_change as pso
import networkx as nx



# # 计算某个节点在某个网络中的结构角色(结构拓扑势)
# impact = 1
# def compute_structural_role(G, node_i):
#     structural_role_i = 0
#     for node_j in nx.nodes(G):
#         if (node_j != node_i):
#             # 获得网络G中其他节点的度数
#             mj = G.in_degree(node_j) + G.out_degree(node_j)
#             # 获得网络中节点间加权最短距离
#             dk = nx.dijkstra_path_length(G, node_i, node_j)  # 最短加权路径长度
#             # 最短加权路径的边的权重之和
#             shortest_path_list = nx.dijkstra_path(G, node_i, node_j)
#             wk = 0
#             for i in range(len(shortest_path_list)-1):
#                 wk = wk + G.get_edge_data(shortest_path_list[i], shortest_path_list[i+1]).values()
#             wij = dk / wk
#
#             # 利用高斯势函数定义节点i的结构角色重要性
#             structural_role_i = structural_role_i + mj*math.exp(-math.pow(wij/impact,2))
#     return structural_role_i / nx.number_of_nodes(G)

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
            dk = shortest_path_length_dict[node_j]
            # 最短加权路径长度(边的权重之和)
            wk = shortest_path_length_weighted_dict[node_j]
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

# 根据0/1列表在邻居列表中筛选需要的列表
def select_neigh_list(x, list):      # x是0/1列表，list是真实列表
    target_list = []
    for i in range(len(list)):
        if(x[i] == 1):
            target_list.append(list[i])
    return target_list

# 加载文件
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\pre_data\rwr\generated_data\het_neigh_train.txt','rb') as edge_file:
    neigh_lines = edge_file.readlines()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\train_data\struct_role_neigh.txt','wb') as f2:
    for index,line in enumerate(neigh_lines):
        struct_role_list = []
        # 去重
        neigh_list = line.decode().split()
        neigh_list_new = remove_same(neigh_list)
        # 调用pso算法进行局部邻居列表的筛选
        pso_object = pso.package(len(neigh_list_new[1:]), neigh_list_new[0], neigh_list_new[1:], index)
        pgd_list = pso_object.run()
        # 用返回的0/1列表在原邻居列表中得到真实的筛选后的列表
        real_list = select_neigh_list(pgd_list, neigh_list_new[1:])

        print("完成了节点", index)

        # 筛选后的列表写入文件
        struct_role_list.append(neigh_list_new[0])
        struct_role_list.extend(real_list[0:])
        line2 = ''
        for j in range(len(struct_role_list)):
            if (j == (len(struct_role_list)-1)):
                line2 = line2 + str(struct_role_list[j]) + '\n'
            else:
                line2 = line2 + str(struct_role_list[j]) + ' '
        print(line2)
        f2.write(line2.encode())
        print("已写入文件")








