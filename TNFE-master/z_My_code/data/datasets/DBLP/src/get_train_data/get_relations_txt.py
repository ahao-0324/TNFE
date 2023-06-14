import pickle
import numpy as np
import networkx as nx

with open(r'D:\Program Files\PycharmProjects\pythonProject\NSHE-master\z_My_code\data\datasets\APS\pre_data\rwr\graph.pkl', 'rb') as fr:
    G = pickle.load(fr)
fr.close()

# 根据node2id文件，获得节点名字及其id对应的字典
node2id_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\NSHE-master\z_My_code\data\datasets\APS\pre_data\train_data\node2id.txt', 'rb') as fn:
    next(fn)
    lines = fn.readlines()
    for line in lines:
        str_list = line.decode().split('\t')
        node2id_dict.update({str_list[0]:str_list[1]})
fn.close()

# 遍历图的边关系，并为不同类型的边做标记
with open(r'D:\Program Files\PycharmProjects\pythonProject\NSHE-master\z_My_code\data\datasets\APS\pre_data\train_data\relations.txt','wb') as f2:
    for edge in nx.edges(G):
        left_id = node2id_dict[edge[0]]
        right_id = node2id_dict[edge[1]]
        relation = list(G.get_edge_data(edge[0], edge[1]).keys())
        if(str(relation[0]) == '1'):
            relation_new = '0'
        if (str(relation[0]) == '2' or str(relation[0]) == '3'):
            relation_new = '1'
        if (str(relation[0]) == '4'):
            relation_new = '2'
        if (str(relation[0]) == '5' or str(relation[0]) == '8' or str(relation[0]) == '9'):
            relation_new = '3'
        if (str(relation[0]) == '6' or str(relation[0]) == '7'):
            relation_new = '4'
        if (str(relation[0]) == '10'):
            relation_new = '5'
        if (str(relation[0]) == '11'):
            relation_new = '6'
        line2 = left_id.replace("\n", "") + '\t' + right_id.replace("\n", "") + '\t' + relation_new + '\n'
        f2.write(line2.encode())
f2.close()
