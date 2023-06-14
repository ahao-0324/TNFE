"""
Model  : SI-HDGNN
Author : Xovee Xu
Date   : Year 2021
"""
import os

P_n = 16408
A_n = 700
V_n = 10


# file paths
pre_data_path = './pre_data/'

# # base files
base_path = 'progress/'
a_p_lst = pre_data_path + base_path + 'a_p_list_progress.txt'
p_a_lst = pre_data_path + base_path + 'p_a_list_progress.txt'
p_v_lst = pre_data_path + base_path + 'p_v_progress.txt'
v_p_lst = pre_data_path + base_path + 'v_p_list_train_progress.txt'
p_p_citation_lst = pre_data_path + base_path + 'p_p_citation_list_progress.txt'
p_date_lst = pre_data_path + base_path + 'paper_date_list.txt'

p_title_emb = pre_data_path + base_path + 'aps_title_emb.pkl'
het_random_walk = pre_data_path + base_path + 'het_random_walk.txt'
het_neigh_train = pre_data_path + base_path + 'het_neigh_train.txt'

# # graph rwr file
rwr_path = 'rwr/'
graph = pre_data_path + rwr_path + 'graph.pkl'
a_neigh = pre_data_path + rwr_path + 'a_neigh.npy'
a_neigh_w = pre_data_path + rwr_path + 'a_neigh_w.npy'
p_neigh = pre_data_path + rwr_path + 'p_neigh.npy'
p_neigh_w = pre_data_path + rwr_path + 'p_neigh_w.npy'

# # gnn train files
gnn_train_path = 'gnn_train_files/'
gnn_pre_file = pre_data_path + gnn_train_path + 'pre_file.pkl'
gnn_node_emb = pre_data_path + gnn_train_path + 'node_embedding.txt'


# A & P prediction common files
prediction_path = pre_data_path + 'prediction_files/'
prediction_common_path = 'prediction_common_files/'

p2_cited_citing_lst = prediction_path + prediction_common_path \
                      + 'p2_cited_citing_list.txt'
p20_cited_citing_lst = prediction_path + prediction_common_path \
                       + 'p20_cited_citing_list.txt'

a2_cited_citing_lst = prediction_path + prediction_common_path \
                      + 'a2_cited_citing_list.txt'
a20_cited_citing_lst = prediction_path + prediction_common_path \
                       + 'a20_cited_citing_list.txt'
author_Prediction_partition = prediction_path + prediction_common_path \
                              + 'paper_addition.pkl'


# hyper-settings
author_length = 6
seq_length = 100
min_citations = 4
# author add
max_papers = 15
