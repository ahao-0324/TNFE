# 先得到表示各种节点间关系的txt文件，然后根据txt文件来构建加权异构图
import sys
import os
BASE_PATH = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(BASE_PATH)
import pickle
import networkx as nx
from itertools import islice

a_relation = [0]      # ap
p_relation = [1, 2]   # pa, pv
v_relation = [3]      # vp

# 得到节点和id对应的字典
id2node_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\train_data\node2id.txt', 'r') as f1:
    for line in islice(f1, 1, None):
        line = line.strip()
        node = line.split('\t')[0]
        id = line.split('\t')[1]
        id2node_dict[id] = node

g = nx.MultiDiGraph()      # 创建多重有向图

# 读取节点关系列表
# a_p_dict = dict()
# p_v_dict = dict()
# p_list = []
# v_list = []
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\train_data\relations.txt', 'r') as f2:
    for line in f2:
        line = line.strip()
        if (line.split('\t')[2] == '0'):
            p_node = id2node_dict[line.split('\t')[0]]
            a_node = id2node_dict[line.split('\t')[1]]
            g.add_edge(a_node, p_node, key=a_relation[0], w=1)
            g.add_edge(p_node, a_node, key=p_relation[0], w=1)
        if (line.split('\t')[2] == '1'):
            p_node = id2node_dict[line.split('\t')[0]]
            v_node = id2node_dict[line.split('\t')[1]]
            g.add_edge(p_node, v_node, key=p_relation[1], w=1)
            g.add_edge(v_node, p_node, key=v_relation[0], w=1)

print('Adding paper&venue nodes and edges to graph G!')
print('Number of nodes', g.number_of_nodes())
print('Number of edges', g.number_of_edges())

print('Save graph G!')

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\pre_data\rwr\ACM_graph.pkl', 'wb') as f:
    pickle.dump(g, f)

#         nextline = next(f2)
#         nextline = nextline.strip()
#         if (line.split('\t')[2] == '0'):
#             # 连续两行节点相同，说明都是该节点的邻居
#             if(line.split('\t')[0] == nextline.split('\t')[0]):
#                 # 将该节点的所有邻居保存到列表中
#                 p_node = id2node_dict[line.split('\t')[1]]
#                 p_list.append(p_node)
#             else:
#                 a_node = id2node_dict[line.split('\t')[0]]
#                 p_node = id2node_dict[line.split('\t')[1]]
#                 p_list.append(p_node)
#                 a_p_dict[a_node] = p_list
#                 p_list = []
#
#         if (line.split('\t')[2] == '1'):
#             if (line.split('\t')[1] == nextline.split('\t')[1]):
#                 v_node = id2node_dict[line.split('\t')[1]]
#                 v_list.append(v_node)
#             else:
#                 p_node = id2node_dict[line.split('\t')[0]]
#                 v_node = id2node_dict[line.split('\t')[1]]
#                 v_list.append(v_node)
#                 p_v_dict[p_node] = v_list
#                 v_list = []
#
# print(a_p_dict)
# print(p_v_dict)