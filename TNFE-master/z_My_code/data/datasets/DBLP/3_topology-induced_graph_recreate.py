# 根据得到的每个节点间拓扑邻居相似度，来对原始图的边权进行重构

import pickle
import networkx as nx
import numpy as np
from itertools import islice

wasserstein_matrix = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\topological_neighbor_similarity_calculate\generated_data\dblp_power_filtration_wasserstein_distances.npy')
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\dblp_graph.pkl', 'rb') as fr:
    g = pickle.load(fr)
nodes = nx.nodes(g)   # 以列表形式返回，列表中的元素是节点名
edges = nx.edges(g)   # 列表中的每个元素是元组，形式是 [('p275686', 'a110250'),('v9', 'p289092')……]

# 查看顶点间边的信息，以字典形式展现，如{11: {'w': 1},12: {'w':3}}，11表示key，即该边属于哪种关系，后面的w:1是边的权重
# 如果在创建图的时候没有设定key的值，那么调用get_edge_data函数时就不会现实key的值，即{{'w': 1}, {'w':3}}
# weight = g.get_edge_data('v9', 'p289092')
# print(weight)


# 获得节点名字和其数字对应的字典
node2id_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\train_data\node2id.txt', 'r') as f1:
    for line in islice(f1, 1, None):
        line = line.strip()
        node = line.split('\t')[0]
        id = line.split('\t')[1]
        node2id_dict[node] = int(id)


#获得节点间边的权重以及边的类型
def get_weight(source, target, G):
    weight = 0
    w_type = 0
    if(source[0] == 'a'):
        if (target[0] == 'p'):
            if g.get_edge_data(source, target) != None:   # 节点间的权重非空
                weight = G.get_edge_data(source, target)[0]['w']
                w_type = 0
            else:
                weight = 0
                w_type = 0
        elif (target[0] == 'a'):   ######
            w_type = 4
        else:   # 创建的异构图中无这类关系
            weight = 999
            w_type = 999
    if (source[0] == 'p'):
        if (target[0] == 'a'):
            if g.get_edge_data(source, target) != None:  # 节点间的权重非空
                weight = G.get_edge_data(source, target)[1]['w']
                w_type = 1
            else:
                weight = 0
                w_type = 1
        elif (target[0] == 'v'):
            if g.get_edge_data(source, target) != None:  # 节点间的权重非空
                weight = G.get_edge_data(source, target)[2]['w']
                w_type = 2
            else:
                weight = 0
                w_type = 2
        elif (target[0] == 'p'):   #####
            w_type = 5
        else:
            weight = 999
            w_type = 999
    if (source[0] == 'v'):
        if (target[0] == 'p'):
            if g.get_edge_data(source, target) != None:  # 节点间的权重非空
                weight = G.get_edge_data(source, target)[3]['w']
                w_type = 3
            else:
                weight = 0
                w_type = 3
        else:
            weight = 999
            w_type = 999
    return weight, w_type

# 获得节点间边的权重以及边的类型
# def get_weight(source, target, G):
#     weight = 0
#     w_type = 0
#     if(source[0] == 'a'):
#         if (target[0] == 'p'):
#             if g.get_edge_data(source, target) != None:   # 节点间的权重非空
#                 weight = G.get_edge_data(source, target)[0]['w']
#                 w_type = 0
#             else:
#                 weight = 0
#                 w_type = 0
#         elif (target[0] == 'a'):   ######
#             w_type = 2
#         else:   # 创建的异构图中无这类关系
#             weight = 999
#             w_type = 999
#     if (source[0] == 'p'):
#         if (target[0] == 'v'):
#             if g.get_edge_data(source, target) != None:  # 节点间的权重非空
#                 weight = G.get_edge_data(source, target)[1]['w']
#                 w_type = 1
#             else:
#                 weight = 0
#                 w_type = 1
#         elif (target[0] == 'p'):   #####
#             w_type = 3
#         else:
#             weight = 999
#             w_type = 999
#     return weight, w_type


# 对wassertain距离进行归一化处理

# 归一化操作
w_list = []
for source in nodes:
    for target in nodes:
        # 获得节点间的拓扑邻居距离
        wasserstein_weight1 = wasserstein_matrix[node2id_dict[source]][node2id_dict[target]]
        w_list.append(wasserstein_weight1)
mean = np.mean(w_list)
std = np.std(w_list, ddof=1)
def do_normalization(value_w, mu, sigma):
    value_w = (value_w - mu) / sigma
    return value_w


# 进行边的权重的改变
# 设置增加边权重和减少边权重的阈值
added_threshold_down = -0.03    # 比-0.12801424小的太多所以要调小，比-0.1280131小的太少所以要调大
added_threshold_up = -0.01
removed_threshold = 15
idx = 0

list = []
for source in nodes:
    print(idx)
    for target in nodes:
        # 获得节点间的拓扑邻居距离
        wasserstein_weight = do_normalization(wasserstein_matrix[node2id_dict[source]][node2id_dict[target]], mean, std)    # 归一化操作
        # wasserstein_weight = wasserstein_matrix[node2id_dict[source]][node2id_dict[target]]

        # 获得此时节点间的边权重及边的类型
        weight, w_type = get_weight(source, target, g)
        # 剔除aa，vv，av，va这些关系
        if (weight != 999 and w_type != 999):
            # 在阈值内，则增加边权重，或者添加边
            if (added_threshold_down < wasserstein_weight < added_threshold_up):
                # 此时两节点有边，则增加权重
                if g.get_edge_data(source, target) != None:
                    # 更新边权
                    g[source][target][w_type]['w'] = weight + wasserstein_weight*10
                # 两节点没有边，则添加边
                else:
                    if(g.get_edge_data(target, source) == None):
                        if(w_type == 4 or w_type == 5):   # 仅针对aa类型和pp类型关系添加边
                            g.add_edge(source, target, key=w_type, w=1)


            # 不在阈值内，则减少边
            if (wasserstein_weight > removed_threshold):
                new_weight = weight - wasserstein_weight/18
                # 更新后的边权重大于0，则更新边权
                if(new_weight > 0):
                    # 此时两节点有边，则减少边的权重
                    if g.get_edge_data(source, target) != None:
                        g[source][target][w_type]['w'] = new_weight
                    else:
                        continue
                # 更新后的边权重小于0，则将原权重设为0
                else:
                    if g.get_edge_data(source, target) != None:
                        g[source][target][w_type]['w'] = 0.001
                    else:
                        continue

    idx = idx + 1

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\topology_induced_graph.pkl', 'wb') as f:
    pickle.dump(g, f)


