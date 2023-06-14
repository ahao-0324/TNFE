import pickle
import numpy as np
import networkx as nx


author_list = []
# 获得作者列表
with open(r'D:\Program Files\PycharmProjects\pythonProject\NSHE-master\z_My_code\data\datasets\APS\pre_data\progress\a_p_list_progresss.txt','rb') as fa:
    lines = fa.readlines()
    for line in lines:
        author_id = 'a' + line[0:(line.decode().index(':'))].decode()
        author_list.append(author_id)
fa.close()

# 获得论文列表
paper_list = []
with open(r'D:\Program Files\PycharmProjects\pythonProject\NSHE-master\z_My_code\data\datasets\APS\pre_data\progress\p_p_citation_list_progress.txt','rb') as fp:
    lines = fp.readlines()
    for line in lines:
        paper_id = 'p' + line[0:(line.decode().index(':'))].decode()
        paper_list.append(paper_id)
fp.close()

# 出版机构列表
v_list = ['v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9']

idx = 0
with open(r'D:\Program Files\PycharmProjects\pythonProject\NSHE-master\z_My_code\data\datasets\APS\pre_data\train_data\node2id.txt','wb') as f2:
    for i in range(len(author_list)):
        line = author_list[i] + '\t' + str(idx) + '\n'
        idx = idx + 1
        f2.write(line.encode())
    print('作者列表处理完成')
    for j in range(len(paper_list)):
        line2 = paper_list[j] + '\t' + str(idx) + '\n'
        idx = idx + 1
        f2.write(line2.encode())
    print('论文列表处理完成')
    for k in range(len(v_list)):
        line3 = v_list[k] + '\t' + str(idx) + '\n'
        idx = idx + 1
        f2.write(line3.encode())
    print('机构列表处理完成')
f2.close()

