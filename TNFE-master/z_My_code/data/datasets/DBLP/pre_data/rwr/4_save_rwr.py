# 该代码的意思是在刚才构建的异构图中进行重启随机游走，得到每种类型节点的邻居集合，然后保存下来

import sys
import os
BASE_PATH = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(BASE_PATH)
import pickle
import math
import numpy as np
from itertools import islice

# input graph
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\topology_induced_graph.pkl', 'rb') as f:
    g = pickle.load(f)


# 获得节点名字和其顺序数字id对应的字典
a_node2id_dict = dict()
a_id2node_dict = dict()
p_node2id_dict = dict()
p_id2node_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\train_data\node2id.txt', 'r') as f1:
    for line in islice(f1, 1, None):
        line = line.strip()
        node = line.split('\t')[0]
        id = line.split('\t')[1]
        if(node[0] == 'a'):
            a_node2id_dict[node] = 'a' + id
            a_id2node_dict['a' + id] = node
        if(node[0] == 'p'):
            p_new_number_id = int(id) - 2000
            p_node2id_dict[node] = 'p' + str(p_new_number_id)
            p_id2node_dict['p' + str(p_new_number_id)] = node




P_n = 9556   # 各种类型节点的总数
A_n = 2000
V_n = 20

a_neigh = [[] for k in range(A_n)]
p_neigh = [[] for k in range(P_n)]
v_neigh = [[] for k in range(V_n)]

a_neigh_w = [[] for k in range(A_n)]
p_neigh_w = [[] for k in range(P_n)]
v_neigh_w = [[] for k in range(V_n)]

a_percent = [1]
# probability
# a_percent[0]: author write paper
# a_percent[1]: author cite paper
# a_percent[3]: author cooperate with author
# a_percent[4]: author publish in venue
for num in range(A_n):
    nod = a_id2node_dict['a' + str(num)]   # 得到a类型节点名字，由于需要遍历该节点邻居，所以需要转化一下
    a_p_write_list = []
    a_p_write_list_w = []

    a_p_cite_list = []
    a_p_cite_list_w = []

    a_a_cooperate_list = []
    a_a_cooperate_list_w = []

    a_v_write_list = []
    a_v_write_list_w = []

    all_node_list = []
    all_weight_list = []

    w_a_p_write = 0
    w_a_p_cite = 0
    w_a_a_cooperate = 0
    w_a_v_write = 0

    # author node
    for i in g[nod]:  # i:neighbor
        for j in g[nod][i]:  # j:key relation
            if int(j) == 0:
                a_p_write_list.append(p_node2id_dict[i])    # 将a的p类型邻居添加进列表，由于需要顺序的p类型节点，所以需要转化一下
                a_p_write_list_w.append(g[nod][i][0]['w'] * math.log(g.in_degree(i)+1))

            # elif int(j) == 1:
            #     a_p_cite_list.append(id_number_dict[i])
            #     a_p_cite_list_w.append(g[nod][i][1]['w'] * math.log(g.in_degree(i)+1))
            #
            # elif int(j) == 3:
            #     a_a_cooperate_list.append(i)
            #     a_a_cooperate_list_w.append(g[nod][i][3]['w'] + math.log(g.in_degree(i)+1))
            #
            # elif int(j) == 4:
            #     a_v_write_list.append(i)
            #     a_v_write_list_w.append(g[nod][i][4]['w'] * math.log(g.in_degree(i)+1))
    w_a_p_write = sum(a_p_write_list_w)
    # w_a_p_cite = sum(a_p_cite_list_w)
    # w_a_a_cooperate = sum(a_a_cooperate_list_w)
    # w_a_v_write = sum(a_v_write_list_w)

    for k in range(len(a_p_write_list)):
        all_node_list.append(a_p_write_list[k])
        all_weight_list.append(float(a_p_write_list_w[k]) / w_a_p_write * a_percent[0])
    # for k in range(len(a_p_cite_list)):
    #     all_node_list.append(a_p_cite_list[k])
    #     all_weight_list.append(float(a_p_cite_list_w[k]) / w_a_p_cite * a_percent[1])
    # for k in range(len(a_a_cooperate_list)):
    #     all_node_list.append(a_a_cooperate_list[k])
    #     all_weight_list.append(float(a_a_cooperate_list_w[k]) / w_a_a_cooperate * a_percent[3])
    # for k in range(len(a_v_write_list)):
    #     all_node_list.append(a_v_write_list[k])
    #     all_weight_list.append(float(a_v_write_list_w[k]) / w_a_v_write * a_percent[4])

    a_neigh[num] = all_node_list
    a_neigh_w[num] = all_weight_list

    if num % 100 == 0:
        print(num, A_n)

save_a_neigh = np.array(a_neigh, dtype="object")
save_a_neigh_w = np.array(a_neigh_w, dtype="object")
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\a_neigh.npy', 'wb') as f:
    np.save(f, save_a_neigh)
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\a_neigh_w.npy', 'wb') as f:
    np.save(f, save_a_neigh_w)


p_percent = [0.6, 0.4]
# probability
# p_percent[0]: paper written by author
# p_percent[1]: paper cite paper
# p_percent[2]: paper cited by paper
# p_percent[3]: paper cite author
# p_percent[4]: paper cited by author
# p_percent[5]: paper publish in venue
for num in range(0, P_n):

    nod = p_id2node_dict['p' + str(num)]   # 获得p类型节点名称

    p_a_writed_list = []
    p_a_writed_list_w = []

    p_p_cite_list = []
    p_p_cite_list_w = []

    p_p_cited_list = []
    p_p_cited_list_w = []

    p_a_cite_list = []
    p_a_cite_list_w = []

    p_a_cited_list = []
    p_a_cited_list_w = []

    p_v_published_list = []
    p_v_published_list_w = []

    all_node_list = []
    all_weight_list = []

    w_p_a_writed = 0
    w_p_p_cite = 0
    w_p_p_cited = 0
    w_p_a_cite = 0
    w_p_a_cited = 0
    w_p_v_published = 0

    # paper node
    for i in g[nod]:  # i:nod节点的neighbor
        for j in g[nod][i]:  # j:key relation
            if int(j) == 1:
                p_a_writed_list.append(a_node2id_dict[i])   # 将p的a类型邻居添加进列表，由于需要顺序的a类型节点，所以需要转化一下
                p_a_writed_list_w.append(g[nod][i][1]['w'] * math.log(g.in_degree(i))+1)
            # elif int(j) == 6:   # 关系6和7是针对p-p的关系，所以只需要对6和7变化
            #     p_p_cite_list.append(id_number_dict[i])
            #     p_p_cite_list_w.append(g[nod][i][6]['w'])
            # elif int(j) == 7:
            #     p_p_cited_list.append(id_number_dict[i])
            #     p_p_cited_list_w.append(g[nod][i][7]['w'] + g.in_degree(i)+1)
            # elif int(j) == 8:
            #     p_a_cite_list.append(i)
            #     p_a_cite_list_w.append(g[nod][i][8]['w'] * math.log(g.in_degree(i))+1)
            # elif int(j) == 9:
            #     p_a_cited_list.append(i)
            #     p_a_cited_list_w.append(g[nod][i][9]['w'] * g.in_degree(i))
            elif int(j) == 2:
                p_v_published_list.append(i)   # v名字已经是顺序的，所以无需转化
                p_v_published_list_w.append(g[nod][i][2]['w'])
                w_p_v_published = w_p_v_published + g[nod][i][2]['w']

    w_p_a_writed = sum(p_a_writed_list_w)
    w_p_p_cite = sum(p_p_cite_list_w)
    w_p_p_cited = sum(p_p_cited_list_w)
    w_p_a_cite = sum(p_a_cite_list_w)
    w_p_a_cited = sum(p_a_cited_list_w)

    for k in range(len(p_a_writed_list)):
        all_node_list.append(p_a_writed_list[k])
        all_weight_list.append(float(p_a_writed_list_w[k]) / w_p_a_writed * p_percent[0])
    # for k in range(len(p_p_cite_list)):
    #     all_node_list.append(p_p_cite_list[k])
    #     all_weight_list.append(float(p_p_cite_list_w[k]) / w_p_p_cite * p_percent[1])
    # for k in range(len(p_p_cited_list)):
    #     all_node_list.append(p_p_cited_list[k])
    #     all_weight_list.append(float(p_p_cited_list_w[k]) / w_p_p_cited * p_percent[2])
    # for k in range(len(p_a_cite_list)):
    #     all_node_list.append(p_a_cite_list[k])
    #     all_weight_list.append(float(p_a_cite_list_w[k]) / w_p_a_cite * p_percent[3])
    # for k in range(len(p_a_cited_list)):
    #     all_node_list.append(p_a_cited_list[k])
    #     all_weight_list.append(float(p_a_cited_list_w[k]) / w_p_a_cited * p_percent[4])
    for k in range(len(p_v_published_list)):
        all_node_list.append(p_v_published_list[k])
        all_weight_list.append(float(p_v_published_list_w[k]) / w_p_v_published * p_percent[1])

    p_neigh[num] = all_node_list
    p_neigh_w[num] = all_weight_list
    if num % 100 == 0:
        print(num, P_n)

save_p_neigh = np.array(p_neigh, dtype="object")
save_p_neigh_w = np.array(p_neigh_w, dtype="object")
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\p_neigh.npy', 'wb') as f:
    np.save(f, save_p_neigh)
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\p_neigh_w.npy', 'wb') as f:
    np.save(f, save_p_neigh_w)
