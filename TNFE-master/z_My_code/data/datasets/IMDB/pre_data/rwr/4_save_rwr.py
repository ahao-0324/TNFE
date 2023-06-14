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
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\topology_induced_graph.pkl', 'rb') as f:
    g = pickle.load(f)




M_n = 3676   # 各种类型节点的总数
A_n = 4353
D_n = 1678

m_neigh = [[] for k in range(M_n)]
a_neigh = [[] for k in range(A_n)]
d_neigh = [[] for k in range(D_n)]

m_neigh_w = [[] for k in range(M_n)]
a_neigh_w = [[] for k in range(A_n)]
d_neigh_w = [[] for k in range(D_n)]

a_percent = [1]
# probability
# a_percent[0]: author write paper
# a_percent[1]: author cite paper
# a_percent[3]: author cooperate with author
# a_percent[4]: author publish in venue
for num in range(A_n):
    nod ='a' + str(num)   # 得到a类型节点名字，由于需要遍历该节点邻居，所以需要转化一下
    a_m_write_list = []
    a_m_write_list_w = []

    a_m_cite_list = []
    a_m_cite_list_w = []

    a_a_cooperate_list = []
    a_a_cooperate_list_w = []

    a_d_write_list = []
    a_d_write_list_w = []

    all_node_list = []
    all_weight_list = []

    w_a_m_write = 0
    w_a_m_cite = 0
    w_a_a_cooperate = 0
    w_a_d_write = 0

    # author node
    for i in g[nod]:  # i:neighbor
        for j in g[nod][i]:  # j:key relation
            if int(j) == 0:
                a_m_write_list.append(i)    # 将a的p类型邻居添加进列表，由于需要顺序的p类型节点，所以需要转化一下
                a_m_write_list_w.append(g[nod][i][0]['w'] * math.log(g.in_degree(i)+1))

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
    w_a_m_write = sum(a_m_write_list_w)
    # w_a_p_cite = sum(a_p_cite_list_w)
    # w_a_a_cooperate = sum(a_a_cooperate_list_w)
    # w_a_v_write = sum(a_v_write_list_w)

    for k in range(len(a_m_write_list)):
        all_node_list.append(a_m_write_list[k])
        all_weight_list.append(float(a_m_write_list_w[k]) / w_a_m_write * a_percent[0])
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
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\generated_data\a_neigh.npy', 'wb') as f:
    np.save(f, save_a_neigh)
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\generated_data\a_neigh_w.npy', 'wb') as f:
    np.save(f, save_a_neigh_w)


m_percent = [0.6, 0.4]
# probability
# p_percent[0]: paper written by author
# p_percent[1]: paper cite paper
# p_percent[2]: paper cited by paper
# p_percent[3]: paper cite author
# p_percent[4]: paper cited by author
# p_percent[5]: paper publish in venue
for num in range(0, M_n):

    nod = 'm' + str(num)   # 获得p类型节点名称

    m_a_writed_list = []
    m_a_writed_list_w = []

    m_m_cite_list = []
    m_m_cite_list_w = []

    m_m_cited_list = []
    m_m_cited_list_w = []

    m_a_cite_list = []
    m_a_cite_list_w = []

    m_a_cited_list = []
    m_a_cited_list_w = []

    m_d_published_list = []
    m_d_published_list_w = []

    all_node_list = []
    all_weight_list = []

    w_m_a_writed = 0
    w_m_m_cite = 0
    w_m_m_cited = 0
    w_m_a_cite = 0
    w_m_a_cited = 0
    w_m_d_published = 0

    # paper node
    for i in g[nod]:  # i:nod节点的neighbor
        for j in g[nod][i]:  # j:key relation
            if int(j) == 1:
                m_a_writed_list.append(i)   # 将p的a类型邻居添加进列表，由于需要顺序的a类型节点，所以需要转化一下
                m_a_writed_list_w.append(g[nod][i][1]['w'] * math.log(g.in_degree(i))+1)
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
                m_d_published_list.append(i)   # v名字已经是顺序的，所以无需转化
                m_d_published_list_w.append(g[nod][i][2]['w'])
                w_m_d_published = w_m_d_published + g[nod][i][2]['w']

    w_m_a_writed = sum(m_a_writed_list_w)
    w_m_m_cite = sum(m_m_cite_list_w)
    w_m_m_cited = sum(m_m_cited_list_w)
    w_m_a_cite = sum(m_a_cite_list_w)
    w_m_a_cited = sum(m_a_cited_list_w)

    for k in range(len(m_a_writed_list)):
        all_node_list.append(m_a_writed_list[k])
        all_weight_list.append(float(m_a_writed_list_w[k]) / w_m_a_writed * m_percent[0])
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
    for k in range(len(m_d_published_list)):
        all_node_list.append(m_d_published_list[k])
        all_weight_list.append(float(m_d_published_list_w[k]) / w_m_d_published * m_percent[1])

    m_neigh[num] = all_node_list
    m_neigh_w[num] = all_weight_list
    if num % 100 == 0:
        print(num, M_n)

save_m_neigh = np.array(m_neigh, dtype="object")
save_m_neigh_w = np.array(m_neigh_w, dtype="object")
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\generated_data\p_neigh.npy', 'wb') as f:
    np.save(f, save_m_neigh)
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\IMDB\pre_data\rwr\generated_data\p_neigh_w.npy', 'wb') as f:
    np.save(f, save_m_neigh_w)
