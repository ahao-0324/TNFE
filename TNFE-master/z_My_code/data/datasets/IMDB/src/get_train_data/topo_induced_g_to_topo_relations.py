# 将3重构的拓扑诱导图转化为模型训练时的与relations格式相同的文件

import networkx as nx
import pickle
import numpy as np
from itertools import islice

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\topology_induced_graph.pkl','rb') as fr:
    G = pickle.load(fr)


# 判断节点间的关系
def get_relation(node1, node2):
    relation = 0
    if(node1[0] == 'a'):
        if(node2[0] == 'm'):
            relation = 0
        if (node2[0] == 'a'):
            relation = 4
    if(node1[0] == 'm'):
        if(node2[0] == 'a'):
            relation = 1
        if (node2[0] == 'd'):
            relation = 2
        if (node2[0] == 'm'):
            relation = 5
    if (node1[0] == 'd'):
        if (node2[0] == 'm'):
            relation = 3
    return relation

# 得到节点和id对应的字典
node2id_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\train_data\node2id.txt', 'r') as f1:
    for line in islice(f1, 1, None):
        line = line.strip()
        node = line.split('\t')[0]
        id = line.split('\t')[1]
        node2id_dict[node] = id

idx = 0
aa_number = 0
pp_number = 0
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\train_data\topo_relaiton.txt','wb') as f2:
    # G.adjacency()格式如下
    # p10584 表示节点
    # {'a2939': {1: {'w': 1}}, 'v2': {2: {'w': 1}}}   表示节点的邻居字典
    for node, nbr_dict in G.adjacency():
        print(idx)
        for nbr in nbr_dict.keys():
            node_id = node2id_dict[node]
            nbr_id = node2id_dict[nbr]
            relation = str(get_relation(node, nbr))
            if(relation == '1' or relation == '2'):
                # 写入文件
                line2 = node_id.replace("\n", "") + '\t' + nbr_id.replace("\n", "") + '\t' + relation + '\n'
                f2.write(line2.encode())
            if (relation == '4' and aa_number < 400):   # 控制要重构的边的数量，不能太多
                aa_number = aa_number + 1
                # 写入文件
                line2 = node_id.replace("\n", "") + '\t' + nbr_id.replace("\n", "") + '\t' + relation + '\n'
                f2.write(line2.encode())
            if (relation == '5' and pp_number < 50):   # 控制要重构的边的数量，不能太多
                pp_number = pp_number + 1
                # 写入文件
                line2 = node_id.replace("\n", "") + '\t' + nbr_id.replace("\n", "") + '\t' + relation + '\n'
                f2.write(line2.encode())
        idx = idx + 1
f2.close()

