import sys
import os
BASE_PATH = os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(BASE_PATH)
import random
import numpy as np
import z_My_code.data.config as config
from itertools import islice

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

P_n = 9556
A_n = 2000
V_n = 20

a_neigh_list_train = [[] for k in range(A_n)]   # A_n是作者节点总数，所以该列表保存的是所有作者节点空列表，每个空列表代表一个作者节点邻居
p_neigh_list_train = [[] for k in range(P_n)]
v_neigh_list_train = [[] for k in range(V_n)]
node_n = [A_n, P_n, V_n]

# load saved rwr files
a_neigh = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\a_neigh.npy',allow_pickle=True)
a_neigh_w = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\a_neigh_w.npy',allow_pickle=True)
p_neigh = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\p_neigh.npy',allow_pickle=True)
p_neigh_w = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\p_neigh_w.npy',allow_pickle=True)

len_limit ={}
len_limit['a'] = 40
len_limit['p'] = 45
len_limit['v'] = 15


len_apv = {}
for i in range(2):   # i取0,1
    for j in range(node_n[i]):  # 所以j取得就是，0-a节点总数，0-p节点总数，0-v节点总数
        if i == 0:
            neigh_train = a_neigh_list_train[j]
            curNode = "a" + str(j)    # 不断将所有的作者节点id赋值给curNode，所以curNode表示当前遍历到的节点
        elif i == 1:
            neigh_train = p_neigh_list_train[j]
            curNode = "p" + str(j)    # j是从2000开始计数
        neigh_L = 0
        len_apv['a'] = 0
        len_apv['p'] = 0
        len_apv['v'] = 0
        rej_times = 0
        while neigh_L < 99:  # maximum neighbor size = 100
            if rej_times >= 150:
                    if len_apv['a'] > 0 and len_apv['p'] > 0 and len_apv['v'] > 0:
                        break
                    elif rej_times >= 300:
                        print(j)
                        break
            rand_p = random.random()  # return p
            if rand_p > 0.5:
                if curNode[0] == "a":
                    chooseNode = random.choices(a_neigh[int(curNode[1:])], a_neigh_w[int(curNode[1:])])[0]
                    if chooseNode[1:] != '':
                        if len_apv[chooseNode[0]] <= len_limit[chooseNode[0]]:
                            # 将经过有偏rwr得到的节点添加到列表中
                            neigh_train.append(chooseNode)
                            curNode = chooseNode
                            len_apv[curNode[0]] += 1
                            neigh_L += 1
                        else:
                            rej_times += 1
                            continue
                    else:
                        continue

                elif curNode[0] == "p":
                    chooseNode = random.choices(p_neigh[int(curNode[1:])], p_neigh_w[int(curNode[1:])])[0]
                    if chooseNode[1:] != '':
                        if len_apv[chooseNode[0]] <= len_limit[chooseNode[0]]:
                            neigh_train.append(chooseNode)
                            curNode = chooseNode
                            len_apv[curNode[0]] += 1
                            neigh_L += 1
                        else:
                            rej_times += 1
                            continue
                    else:
                        continue

                elif curNode[0] == "v":
                    if i == 0 :
                        curNode = ('a' + str(j))
                    elif i == 1:
                        curNode = ('p' + str(j))

            else:
                if i == 0:
                    curNode = ('a' + str(j))
                elif i == 1:
                    curNode = ('p' + str(j))
        if i == 0:
            curNode = 'a' + str(j)
        elif i == 1:
            curNode = 'p' + str(j)

        if j % 100 == 0:
            print(j, node_n[i])


for i in range(2):
    for j in range(node_n[i]):
        if i == 0:
            a_neigh_list_train[i] = list(a_neigh_list_train[i])
        elif i == 1:
            p_neigh_list_train[j] = list(p_neigh_list_train[j])


neigh_f = open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\DBLP\pre_data\rwr\generated_data\het_neigh_train.txt', "w")
for i in range(2):
    for j in range(node_n[i]):
        if i == 0:
            neigh_train = a_neigh_list_train[j]
            curNode = a_id2node_dict['a' + str(j)]
        elif i == 1:
            neigh_train = p_neigh_list_train[j]
            curNode = p_id2node_dict['p' + str(j)]    # 把顺序的论文id转化为网络中实际的论文id

        if len(neigh_train):
            neigh_f.write(curNode + " ")
            for k in range(len(neigh_train)-1):
                if (neigh_train[k][0] == "p"):
                    neigh_train[k] = p_id2node_dict[neigh_train[k]]
                if (neigh_train[k][0] == "a"):
                    neigh_train[k] = a_id2node_dict[neigh_train[k]]
                neigh_f.write(neigh_train[k] + " ")
            if (neigh_train[-1][0] == "p"):
                neigh_train[-1] = p_id2node_dict[neigh_train[-1]]
            if (neigh_train[-1][0] == "a"):
                neigh_train[-1] = a_id2node_dict[neigh_train[-1]]
            neigh_f.write(neigh_train[-1] + "\n")
neigh_f.close()

# 最后得到的文件形式为：
# 当前节点1 采样节点1 采样节点2 ... 采样节点n
# 当前节点2 采样节点1 采样节点2 ... 采样节点m
# ……
