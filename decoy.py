import pandas as pd
import csv
import selfUtils as su
import numpy as np
from datetime import datetime
import sys

def uni_trace(trace):
    trace_info = []
    out_burst = in_burst = 0
    for p in trace[1:]:
        if p == 0:
            break
        if p == 1:
            trace_info.append(in_burst * -1)
            out_burst += 1
            in_burst = 0

        else:
            trace_info.append(out_burst * 1)
            in_burst += 1
            out_burst = 0
    trace_info = [num for num in trace_info if num]
    return trace_info


def decoy(candidate, sel_trace, start_idx, end_idx):
    candidiate_info = uni_trace(candidate)
    sel_trace_info = uni_trace(sel_trace)
    decoyed=[]
    d_len = min(len(candidiate_info),len(sel_trace_info))
    for i in range(d_len):
        if candidiate_info[i] * sel_trace_info[i] > 0:
            d = max(abs(candidiate_info[i]), abs(sel_trace_info[i]))
            if candidiate_info[i] < 0:
                decoyed.append(-1 * d)
            else:
                decoyed.append(d)
        else:
            decoyed.append(max(candidiate_info[i], sel_trace_info[i]))
            decoyed.append(min(candidiate_info[i], sel_trace_info[i]))
    if len(candidiate_info) > d_len:
        decoyed.extend(candidiate_info[d_len:])
    else:
        decoyed.extend(sel_trace_info[d_len:])

    trace1 = candidate[0:start_idx+1]
    trace2 = sel_trace[0:start_idx+1]

    bursts_sum = busrts_start_idx = busrt_end_idx = 0
    for i, d in enumerate(decoyed):
        bursts_sum += abs(d)
        if bursts_sum >= start_idx:
            busrts_start_idx = i
            bursts_sum = 0
            for ii, dd in enumerate(decoyed[i:]):
                bursts_sum += abs(dd)
                busrt_end_idx = ii + busrts_start_idx
                if bursts_sum >= (end_idx - start_idx):
                    break
            break
    for p in decoyed[busrts_start_idx:busrt_end_idx]:
        if p > 0:
            trace1.extend(abs(p) * [1])
            trace2.extend(abs(p) * [1])
        else:
            trace1.extend(abs(p) * [-1])
            trace2.extend(abs(p) * [-1])
    trace1.extend(candidate[end_idx:])
    trace2.extend(sel_trace[end_idx:])
    trace1 = np.array(trace1)
    trace2 = np.array(trace2)
    pad = lambda a,i: a[0:i] if a.shape[0]>i else np.hstack((a, np.zeros(i-a.shape[0])))
    trace1 = pad(trace1, 5001)
    trace2 = pad(trace2, 5001)

    ori_size = sum([abs(ele) for ele in candidiate_info]) + sum([abs(ele) for ele in sel_trace_info])
    overhead = sum([abs(ele) for ele in trace1[1:]]) + sum([abs(ele) for ele in trace2[1:]]) - ori_size
    with open('wf_decoy_test.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(trace1)
        writer.writerow(trace2)

    return ori_size, overhead


def decoy_all(candidate, sel_trace):
    candidiate_info = uni_trace(candidate)
    sel_trace_info = uni_trace(sel_trace)
    decoyed=[]
    d_len = min(len(candidiate_info),len(sel_trace_info))
    for i in range(d_len):
        if candidiate_info[i] * sel_trace_info[i] > 0:
            d = max(abs(candidiate_info[i]), abs(sel_trace_info[i]))
            if candidiate_info[i] < 0:
                decoyed.append(-1 * d)
            else:
                decoyed.append(d)
        else:
            decoyed.append(max(candidiate_info[i], sel_trace_info[i]))
            decoyed.append(min(candidiate_info[i], sel_trace_info[i]))
    if len(candidiate_info) > d_len:
        decoyed.extend(candidiate_info[d_len:])
    else:
        decoyed.extend(sel_trace_info[d_len:])

    trace1 = [candidate[0]]
    trace2 = [sel_trace[0]]

    for p in decoyed:
        if p > 0:
            trace1.extend(abs(p) * [1])
            trace2.extend(abs(p) * [1])
        else:
            trace1.extend(abs(p) * [-1])
            trace2.extend(abs(p) * [-1])

    trace1 = np.array(trace1)
    trace2 = np.array(trace2)
    pad = lambda a,i: a[0:i] if a.shape[0]>i else np.hstack((a, np.zeros(i-a.shape[0])))
    trace1 = pad(trace1, 5001)
    trace2 = pad(trace2, 5001)

    ori_size = sum([abs(ele) for ele in candidiate_info]) + sum([abs(ele) for ele in sel_trace_info])
    overhead = sum([abs(ele) for ele in trace1[1:]]) + sum([abs(ele) for ele in trace2[1:]]) - ori_size
    with open('wf_decoy_test.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(trace1)
        writer.writerow(trace2)

    return ori_size, overhead


def pair(lists):
    Size = Overhead = 0
    while lists:
        print(datetime.now())
        print(len(lists))
        candidate = lists.pop(0)
        print()
        smallest = 100000
        sel_id = 0
        success = False
        for i,trace in enumerate(lists):
            label1 = candidate[0]
            label2 = trace[0]
            len1 = np.count_nonzero(candidate[1:])
            len2 = np.count_nonzero(trace[1:])
            if label1 != label2:

                distances = [abs(y - x) for x, y in zip(candidate[1:], trace[1:])]
                distance = sum(distances)
                if distance < smallest:
                    smallest = distance
                    sel_id = i
                    success = True
                # with open('distance.csv', 'a') as f:
                #     writer = csv.writer(f)
                #     writer.writerow([label1, label2, distance])
        sel_trace = lists.pop(sel_id)
        # ori_size, _overhead = decoy(candidate, sel_trace, 0, 5000)
        ori_size, _overhead = decoy_all(candidate, sel_trace)
        Size += ori_size
        Overhead += _overhead
    r = Overhead/Size
    with open('decoy_overhead_test.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(r)


def seperate():
    path = '/home/lhp/PycharmProjects/feature_analysis/chunks/1.csv'
    # chunks = []
    # chunksize = 4000
    # # for i in range(95):
    # lists = []
    # # print(datetime.now())
    # for chunk in pd.read_csv(path, chunksize=chunksize):
    #     lists=chunk.values.tolist()
    #     lists.sort(key=su.sort_by_name)
    # path = sys.argv[1]
    df = pd.read_csv(path, header=None)
    lists = df.values.tolist()
    pair(lists)


if __name__ == '__main__':
    seperate()



