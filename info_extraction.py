import selfUtils as su
import pandas as pd
import os
import sys
import numpy as np
import pickle
from pathlib import Path
import csv
import math
from sklearn import preprocessing
import re


def emergency():
    path = '/home/lhp/PycharmProjects/dataset/WF_dataset/wf_incoming.csv'
    chunks = []
    chunksize = 2000
    for chunk in pd.read_csv(path, chunksize=chunksize, header=None):
        chunks.append(chunk)
        print(len(chunks))
    for df in chunks:
        data = df.iloc[:,1:].values.tolist()
        for trace in data:
            cluster_list = []
            size_list = []
            cluster = 0
            size = 0
            for p in trace:
                if p == 0:
                    cluster_list.extend(cluster * [cluster])
                    size_list.extend(cluster * [size])
                    cluster = 0
                    size = 0
                    cluster_list.append(cluster)
                    size_list.append(size)
                else:
                    cluster += 1
                    size += p
            with open('cluster_info_wf.csv', 'a') as w:
                writer = csv.writer(w)
                writer.writerow(cluster_list)
            with open('size_info_wf.csv', 'a') as w:
                writer = csv.writer(w)
                writer.writerow(size_list)


def average(pa):
    path = pa
    sum = 5001 * [0]
    chunks = []
    chunksize = 2000
    for chunk in pd.read_csv(path, chunksize=chunksize):
        chunks.append(chunk)
        print(len(chunks))
    n = len(chunks)

    for df in chunks:
        ave = df.mean(axis=0)
        for i,a in enumerate(ave):
            sum[i] += a
    ave_list = [i/n for i in sum]
    with open('ave_wf.csv', 'a') as w:
        writer = csv.writer(w)
        writer.writerow(ave_list)

def pattern_analyzation():
    path = '/home/lhp/PycharmProjects/dataset/WF_dataset/wf_incoming.csv'
    data = pd.read_csv(path)

    data = data.iloc[:, 1:].values.tolist()

    for trace in data:
        cluster_list = []
        size_list = []
        cluster = 0
        size = 0
        for p in trace:
            if p == 0:
                cluster_list.extend(cluster * [cluster])
                size_list.extend(cluster * [size])
                cluster = 0
                size = 0
                cluster_list.append(cluster)
                size_list.append(size)
            else:
                cluster += 1
                size += p
        with open('cluster_info_wf.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(cluster_list)
        with open('size_info_wf.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(size_list)


def group():
    num = 300
    info_list = pd.read_csv('datafiles/mi_alexa_in.csv')
    mi = info_list.sort_values(by=['mi'], ascending=False)
    top_mi = mi.iloc[:num,0].tolist()
    cluster = info_list.sort_values(by=['cluster'], ascending=False)
    top_cluster = cluster.iloc[:num,0].tolist()
    size = info_list.sort_values(by=['size'], ascending=False)
    top_size = size.iloc[:num,0].tolist()
    results = []
    for p in top_mi:
        if p in top_cluster and p in top_size:
            results.append([p,'all'])
        elif p in top_cluster:
            results.append([p, 'cluster'])
        # elif p in top_size:
        #     results.append([p, 'size'])
        else:
            results.append([p, 'mi'])
    dd = pd.DataFrame(results)
    dd.to_csv('group_wf.csv')


def main():
    # emergency()
    # pattern_analyzation()
    group()
    # average('cluster_info_wf.csv')
    # average('size_info_wf.csv')

if __name__ == '__main__':
    main()