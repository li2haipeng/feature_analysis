import pandas as pd
import csv
import selfUtils as su
import numpy as np
from datetime import datetime
import sys
import random


def length():
    path = 'datafiles/WF_dataset/wf.csv'
    # path = sys.argv[1]
    chunksize = 1000
    lists = []
    for chunk in pd.read_csv(path, chunksize=chunksize):
        lists=chunk.values.tolist()
        lists.sort(key=su.sort_by_name)
        for trace in lists:
            neg = pos = 0
            len_list = [trace[0]]
            for p in trace:
                if p <0:
                    neg += 1
                elif p > 0:
                    pos +=1

            len_list.extend(pos * [1])
            len_list.extend(neg * [-1])
            len_list = np.array(len_list)
            pad = lambda a, i: a[0:i] if a.shape[0] > i else np.hstack((a, np.zeros(i - a.shape[0])))
            len_list = pad(len_list, 5001)
            with open('wf_hd.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(len_list)

def pad_one():
    path = 'datafiles/WF_dataset/wf.csv'
    # path = sys.argv[1]
    chunksize = 1000
    lists = []
    for chunk in pd.read_csv(path, chunksize=chunksize):
        lists = chunk.values.tolist()
        lists.sort(key=su.sort_by_name)

        for trace in lists:
            padded_list = [trace[0]]
            l = np.count_nonzero(trace[1:])
            if l > 1130:
                padded_list.extend(trace[1129:1139])
            else:
                padded_list.extend(10*[0])
            # padded_list.extend(trace[1:l+1])
            # a = random.randint(-1, 1)
            # while len(padded_list) <5001 :
            #     a = random.randint(-1, 1)
            #     # aa = a/abs(a)
            #     if a != 0:
            #         padded_list.extend([a])
            with open('wf_test.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(padded_list)
def cal():
    # data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/wf_test.csv',header=None)
    chunksize = 1000
    lists = []
    count = 0
    for chunk in pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/wf_test.csv', chunksize=chunksize, header=None):
        ave = chunk.mean(axis=0)
        ave = list(ave)
        aaa = [count]+ ave
        count += 1
        with open('ave_test.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(aaa)

if __name__ == '__main__':
    # length()
    # pad_one()
    cal()