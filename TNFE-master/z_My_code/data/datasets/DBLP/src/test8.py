# 测试评估函数，对得到向量进行评估

import argparse
import pickle
import warnings

import numpy as np

from models import NSHE
from hyperparams import Hyperparams
from evaluation import Evaluation
import torch.nn.functional as F
import torch.optim as optim
import time
from util_funcs import *
from hin_loader import HIN

def evaluate(node_emb, t_info):
    # Evaluation
    # Evaluate with random seed
    exp = Evaluation(hp.dataset)
    if hp.dataset == 'imdb':
        res = exp.evaluate_imdb(node_emb[:t_info['m']['cnt']])
    elif hp.dataset == 'dblp':
        res = exp.evaluate_dblp(node_emb)
    elif hp.dataset == 'aps':
        res = exp.evaluate_acm(node_emb)
    print_dict(res)

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='GCN')
    parser.add_argument("--dataset", type=str, default='aps', help="dataset to train")
    parser.add_argument("--task", type=str, default='cla', help="task to train")
    args = parser.parse_args()

    hp = Hyperparams(args.dataset, args.task)
    warnings.filterwarnings('ignore')
    g = HIN(hp)
    # 加载节点向量文件
    node_emb = torch.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\APS\pre_data\model_data\aps\final_embedding.pt')
    node_emb2 = np.load(r'D:\Program Files\PycharmProjects\pythonProject\mycode-master\z_My_code\data\datasets\APS\pre_data\model_data\aps\dw_emb_features.npy')
    # 进行评估
    evaluate(node_emb, g.t_info)
