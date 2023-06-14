# 在得到rwr游走后的文件后，每个节点都有各自对应的邻居节点集合，这里的操作是将这种关系转化为和relations.txt文件相同的格式，每行是两个节点以及他们对应的关系
# 这样就可以送到模型中，去进行网络模式的采样


# 对列表中的元素去重，并按照原先顺序返回
def remove_same(orgList):
    formatList = []
    for id in orgList:
        if id not in formatList:
            formatList.append(id)
    return formatList

# 根据node2id文件，获得节点名字及其id对应的字典
node2id_dict = dict()
with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\train_data\node2id.txt', 'rb') as fn:
    next(fn)
    lines = fn.readlines()
    for line in lines:
        str_list = line.decode().split('\t')
        node2id_dict.update({str_list[0]:str_list[1]})
fn.close()

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\train_data\struct_role_neigh.txt','rb') as edge_file:
    neigh_lines = edge_file.readlines()

with open(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\ACM\train_data\relation_neigh_structrole.txt','wb') as f2:
    for line in neigh_lines:
        # 对列表元素去重
        neigh_list = line.decode().split()
        neigh_list_new = remove_same(neigh_list)

        for i in range(len(neigh_list_new)):
            if(i > 0):
                left_node = neigh_list_new[0]
                right_node = neigh_list_new[i]
                # 判断两个节点间的关系
                if(left_node[0] == 'a' and right_node[0] == 'p'):
                    relation = '0'
                if (left_node[0] == 'p' and right_node[0] == 'a'):
                    relation = '1'
                if (left_node[0] == 'p' and right_node[0] == 'v'):
                    relation = '2'
                if (left_node[0] == 'v' and right_node[0] == 'p'):
                    relation = '3'
                # 获得节点id
                left_id = node2id_dict[left_node]
                right_id = node2id_dict[right_node]
                # 写入文件
                line2 = left_id.replace("\n", "") + '\t' + right_id.replace("\n", "") + '\t' + relation + '\n'
                f2.write(line2.encode())
f2.close()
