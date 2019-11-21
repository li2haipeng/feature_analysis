from __future__ import division
import csv
import pandas as pd
import random


def calculate_ratio(packets):
    s = r = 0
    for p in packets:
        s += p[1]
    for i,p in enumerate(packets):
        if i == 0:
            r = p[1] / s
            p.append(r)
            continue
        r = (p[1] / s) + packets[i - 1][2]
        p.append(r)


def sample_from_distribution(interval_list):
    interval = 0
    # calculate_ratio(size_list)
    # interval_list.sort(key=su.sort_by_third, reverse=True)
    # calculate_ratio(interval_list)

    a = random.randint(0, 99)/100

    for p in interval_list:
        if a <= p[2]:
            interval = p[0]
            break

    return interval


def distribution():
    path = '/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/wf.csv'
    chunks = []
    chunksize = 2000
    neg_interval={}
    pos_interval={}
    for chunk in pd.read_csv(path, chunksize=chunksize):
        chunks.append(chunk)
        print(len(chunks))
    for df in chunks:
        data = df.iloc[:,1:].values.tolist()
        neg_count = 0
        pos_count = 0
        for trace in data:
            for i, p in enumerate(trace):
                if i == len(trace)-1:
                    continue
                if p == -1:
                    neg_count += 1
                    if trace[i+1] == 1:
                        if neg_count in pos_interval:
                            pos_interval[neg_count] += 1
                        else:
                            pos_interval[neg_count] = 1
                        neg_count = 0
                else:
                    pos_count += abs(p)
                    if trace[i+1] == -1:
                        if pos_count in neg_interval:
                            neg_interval[pos_count] += 1
                        else:
                            neg_interval[pos_count] = 1
                        pos_count = 0
    with open('wf_interval_in.csv', 'w') as f:
        writer = csv.writer(f)
        for row in neg_interval.items():
            writer.writerow(row)
    with open('wf_interval_out.csv', 'w') as f:
        writer = csv.writer(f)
        for row in pos_interval.items():
            writer.writerow(row)


def padding(trace, in_inter_list, out_inter_list):
    padded=[]
    label=trace.pop(0)
    padded.append(label)

    in_interval = sample_from_distribution(in_inter_list)
    out_interval = sample_from_distribution(out_inter_list)
    # if in_interval > 1:
    #     in_interval = 1
    # if out_interval > 1:
    #     out_interval = 1
    # in_interval = out_interval = 1
    in_count = 0
    out_count = 0
    out_sum = in_sum = 0
    in_overhead = out_overhead = 0
    for p in trace:
        padded.append(p)
        if p == 1:
            out_sum += 1
            out_count += 1
            in_count = 0
            if out_count >= in_interval:
                in_interval = sample_from_distribution(in_inter_list)
                n = round(in_interval/2)
                padded.extend(n*[-1.0])
                in_overhead += n
                out_count = 0

                # if in_interval > 1:
                #     in_interval = 1
        else:
            in_sum += 1
            in_count += 1
            out_count = 0
            if in_count >= out_interval :
                out_interval = sample_from_distribution(out_inter_list)
                n = round(out_interval/2)
                padded.extend(n*[1.0])
                out_overhead += n
                in_count = 0

                # if out_interval > 1:
                #     out_interval = 1
    with open('wf_overhead_round.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([in_sum, out_sum, in_overhead, out_overhead])
    return padded


def adv_padding(trace, in_inter_list, out_inter_list):
    padded = []
    label = trace.pop(0)
    padded.append(label)

    in_interval = sample_from_distribution(in_inter_list)
    out_interval = sample_from_distribution(out_inter_list)
    # if in_interval > 1:
    #     in_interval = 1
    # if out_interval > 1:
    #     out_interval = 1
    # in_interval = out_interval = 1
    in_count = 0
    out_count = 0
    out_sum = in_sum = 0
    in_overhead = out_overhead = 0
    for p in trace:
        padded.append(p)
        if p == 1:
            out_sum += 1
            out_count += 1
            in_count = 0
            if out_count >= in_interval:
                in_interval = sample_from_distribution(in_inter_list)
                n = in_interval
                padded.extend(n * [-1.0])
                in_overhead += n
                out_count = 0

        else:
            in_sum += 1
            in_count += 1
            out_count = 0
            if in_count >= out_interval:
                out_interval = sample_from_distribution(out_inter_list)
                if out_interval > 4:
                    out_interval = 4
                n = out_interval
                padded.extend(n * [1.0])
                out_overhead += n
                in_count = 0


    with open('wf_overhead_4.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([in_sum, out_sum, in_overhead, out_overhead])
    return padded


if __name__ == '__main__':
    # distribution()
    in_inter_list = pd.read_csv('wf_interval_in.csv',header=None)
    out_inter_list = pd.read_csv('wf_interval_out.csv', header=None)
    in_inter_list = in_inter_list.values.tolist()
    out_inter_list = out_inter_list.values.tolist()
    calculate_ratio(in_inter_list)
    calculate_ratio(out_inter_list)


    path = '/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/wf.csv'
    # chunks = []
    chunksize = 2000
    neg_interval = {}
    pos_interval = {}
    for chunk in pd.read_csv(path, chunksize=chunksize):
        # chunks.append(chunk)
        # print(len(chunks))
        data = chunk.values.tolist()
        for trace in data:
            padded_t = adv_padding(trace, in_inter_list, out_inter_list)
            with open('wf_padded_4.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(padded_t[0:5001])



    # path = 'pad_test.csv'
    # df = pd.read_csv(path, header=None)
    # padded_traces = []
    # trace = df.values.tolist()[0]
    # padded_t = padding(trace, in_inter_list, out_inter_list)
    # padded_traces.append(padded_t)
    # with open('pad_trace.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(padded_t)