import numpy as np
from util import *
from topology import *
import gudhi as gd
import networkx as nx
from persim import wasserstein
import pandas as pd
from itertools import islice
import pickle

# load data, e.g., cora
# dataset = 'cora'
# adj, features, y_train, y_val, y_test, train_mask, val_mask, test_mask, label = load_data(dataset)
# adj_array = adj.toarray().astype(np.float32)
# power filtration, i.e., topological distance

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\dblp_graph.pkl', 'rb') as fr:
    g = pickle.load(fr)

# adj_g = nx.to_numpy_matrix(g)
# adj_array = adj_g.toarray().astype(np.float32)

# 获得节点特征向量矩阵
features_list = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\train_data\dw_emb_features.npy')

# 获得节点名字和其数字对应的字典
node2id_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\train_data\node2id.txt', 'r') as f1:
    for line in islice(f1, 1, None):
        line = line.strip()
        node = line.split('\t')[0]
        id = line.split('\t')[1]
        node2id_dict[node] = int(id)

# To get node_similarity_matrix.npy, please run edge_weight_func on node feature matrix
node_similarity_matrix = edge_weight_func(features_list)
# node_similarity_matrix = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\topological_neighbor_similarity_calculate\generated_data\edge_weight_mat.npy')
k_hop = 1
# # 得到每个节点的k阶邻居加权子图
k_hop_subgraphs = k_th_order_weighted_subgraph(g, w_adj_mat=node_similarity_matrix, k=k_hop, node2id_dict=node2id_dict)
# 这里的节点相似度矩阵，我们需要改变，因为对于异构图来说，不能使用基于节点间属性相似度来得到节点相似度矩阵，应该基于节点的向量表示来得到


power_filtration_dgms = list()
for i in range(len(k_hop_subgraphs)):
    print(i)
    power_filtration_dgm = simplicial_complex_dgm(k_hop_subgraphs[i])      # 根据每个节点的k阶邻居加权子图，可以得到每个节点的单纯复形图
    if power_filtration_dgm.size == 0:
        power_filtration_dgms.append(np.array([]))
    else:
        power_filtration_dgms.append(power_filtration_dgm)

power_dgms = np.array(power_filtration_dgms)


# for any pair of nodes
# wasserstein distances calculation
# 这里可能需要调整，如果矩阵太大无法创建，需要使用txt文件保存，那么就先需要节点id和数字匹配的列表，然后按照之前edge_weight_func的保存方法保存
wasserstein_distances = np.zeros((len(features_list),len(features_list)), dtype = np.float32)
for i in range(len(features_list) - 1):
    print(i)
    for j in range(i+1, len(features_list)):
        wasserstein_distances[i, j] = wasserstein(power_dgms[i], power_dgms[j])    # 基于节点i和节点j的拓扑邻居集合(持续性图)，来计算节点间的wasserstein距离
        wasserstein_distances[j, i] = wasserstein(power_dgms[j], power_dgms[i])    # wasserstein distance is not symmetric

np.save(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\topological_neighbor_similarity_calculate\generated_data\dblp_power_filtration_wasserstein_distances.npy', wasserstein_distances)


# # for k-hop neighborhood
# # wasserstein distances calculation
# k = 3 # only consider calculating the distances between node u and its k-hop neighborhood
# # G = nx.from_numpy_matrix(adj_array)
# wasserstein_distances = np.zeros((len(features_list),len(features_list)), dtype = np.float32)
# for i in range(len(features_list) - 1):
#     v_labels = [name for name, value in nx.single_source_shortest_path_length(g, i, cutoff=k).items()]
#     for j in v_labels:
#         wasserstein_distances[i, j] = wasserstein(power_dgms[i], power_dgms[j])
#         wasserstein_distances[j, i] = wasserstein(power_dgms[j], power_dgms[i]) # wasserstein distance is not symmetric
#
# np.save('_' +  str(k) + '_hop_'+ 'power_filtration_wasserstein_distances', wasserstein_distances)

