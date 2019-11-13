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


def wf_burst():
    # data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/alexa/gamma_binary.csv')
    # # X = data.iloc[:,1:]
    # # y = data.iloc[:,0]
    # X = data.values

    chunk_l = []

    chunksize = 2000
    for chunk in pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/wf.csv',
                             chunksize=chunksize, header=None):
        chunk_l.append(chunk)

    for chunk in chunk_l:
        for trace in chunk.values:
            bursts = [trace[0]]
            n = 1
            for i, p in enumerate(trace):
                if i == 0:
                    continue
                if i == len(trace) - 1:
                    continue
                if trace[i + 1] == p:
                    n += 1
                else:
                    bursts.append(n * p)
                    n = 1
                if trace[i + 1] == 0:
                    break
            with open('wf_burst.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(bursts)
    print()


def distribution():
    path = '/home/lhp/PycharmProjects/dataset/WF_dataset/wf_burst.csv'
    data = pd.read_csv(path, header=None)
    # data = data.values.tolist()
    dis = {}
    for idx, row in data.iterrows():
        l = len(row) - 1 - row.isna().sum()
        if l in dis.keys():
            dis[l] += 1
        else:
            dis[l] = 1
    with open('wf_burst_distribution.csv', 'w') as _t:
        writer = csv.DictWriter(_t, dis.keys())
        writer.writeheader()
        writer.writerow(dis)


def idx_count():
    path = '/home/lhp/PycharmProjects/dataset/WF_dataset/wf_burst.csv'
    data = pd.read_csv(path, header=None)
    data = data.iloc[:, 1:]
    n_sum = p_sum = 0
    for idx, row in data.iterrows():
        new_row = []
        for i in row:
            x = float(i)
            if math.isnan(x):
                break
            if i < 0:
                n_sum += i
            else:
                p_sum += i
            # sum = abs(i) + sum
            r = [i, n_sum, p_sum]
            new_row.append(r)
        n_sum = p_sum = 0
        with open('wf_burst_index_info.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(new_row)


def alexa_burst():
    data = pd.read_csv('/home/lhp/PycharmProjects/dataset/Alexa_dataset/numeric_lable.csv')

    for trace in data.values:
        bursts = [trace[0]]
        burst = 0
        for i, p in enumerate(trace):
            if i == 0:
                continue
            if i == len(trace) - 1:
                continue
            burst += p
            if trace[i + 1] * p > 0:
                pass
            else:
                bursts.append(burst)
                burst = 0
            if trace[i + 1] == 0:
                break
        with open('alexa_burst.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(bursts)
    print()


def numeric():
    data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/alexa_100.csv',header = None)
    y = data.iloc[:, 0]
    le = preprocessing.LabelEncoder()
    labels = le.fit_transform(y)
    data.iloc[:, 0] = labels
    data.to_csv('/home/lhp/PycharmProjects/feature_analysis/alexa_100_numeric.csv', index=False)


def video_burst():
    # path = '/home/lhp/PycharmProjects/dataset/Video_dataset/csv/Gaming/Gaming_01/'
    path = sys.argv[1]
    files = os.listdir(path)
    for f in files:
        fpath = os.path.join(path, f)
        pf = Path(fpath)
        trace_name = pf.name[0:-4]
        nameRegex = re.compile(r'\d_')
        mo = nameRegex.search(trace_name)
        trace_name = trace_name[0: mo.start() + 1]
        data = pd.read_csv(fpath)
        packets = data.values.tolist()
        downloading_packets = []
        for p in packets:
            if p[2] == -1:
                downloading_packets.append(p)
        window = 0.25
        init_time = 0
        bursts = [trace_name]

        burst = 0
        for d_p in downloading_packets:

            if d_p[0] <= init_time + window:
                burst += d_p[1]
            else:
                bursts.append(burst)
                init_time += window
                while d_p[0] > init_time + window:
                    bursts.append(0)
                    init_time += window
                burst = d_p[1]
        with open('video_bin.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(bursts)
    print()


def to_one_file(path):
    files = os.listdir(path)
    files.sort()
    print(len(files))
    for f in files:
        try:
            trace = []
            f_path = os.path.join(path, f)
            fp = Path(f_path)
            trace_name = fp.name[0:-4]
            nameRegex = re.compile(r'\?')
            mo = nameRegex.search(trace_name)
            trace_name = trace_name[0: mo.start()]
            trace.append(trace_name)

            packets = pd.read_csv(f_path)
            size = packets.iloc[:, 1]
            direction = packets.iloc[:, 2]
            size = size.values
            direction = direction.values

            results = np.multiply(size, direction)
            pad = lambda a, i: a[0:i] if a.shape[0] >= i else np.hstack((a, np.zeros(i - a.shape[0])))
            results = pad(results, 400)
            trace = trace.__add__(results.tolist())
            with open('alexa_dp_whole.csv', 'a') as w:
                writer = csv.writer(w)
                writer.writerow(trace)
        except:
            continue
        # print(f + 'is added')
    print(path + ' finished!')


def incoming_selection():
    path = '/home/lhp/PycharmProjects/dataset/WF_dataset/wf.csv'
    data = []

    chunksize = 2000
    for chunk in pd.read_csv(path, chunksize=chunksize, header=None):
        data.append(chunk)
        print(len(data))
    # x = data.iloc[:,1:]
    x_list = data
    for trace in x_list:
        new_trace = [trace[0]]
        for i, p in enumerate(trace):
            if i == 0:
                continue
            size = float(p)
            if size >= 0:
                new_trace.append(0)
            else:
                new_trace.append(-size)

        with open('wf_incoming.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(new_trace)



if __name__ == "__main__":
    # wf_burst()
    # distribution()
    # idx_count()
    # alexa_burst()
    # numeric()
    # video_burst()
    # path = sys.argv[1]
    # # path = '/home/lhp/PycharmProjects/dataset/Alexa_dataset/sel_defense/dp/1'
    # to_one_file(path)
    incoming_selection()
