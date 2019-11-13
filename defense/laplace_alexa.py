from __future__ import division
import sys
sys.path.append('/home/lhp/PycharmProjects/feature_analysis/')
import argparse
import random
from pathlib import Path
import pandas as pd
import selfUtils as su
import csv
from math import log
from scipy.stats import laplace
import queue
import numpy as np
import os


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


def lap_csv(packets, lap_list, eps):
    # lap_list = []
    g = 0
    r = 0
    num = -1
    i = len(lap_list)

    g = su.cal_g(i)
    if i == 1 or i == su.cal_d(i):
        # r = int(np.random.laplace(0, 1/eps))
        r = int(laplace.rvs(0, 1/eps))
    else:
        num = int(log(i, 2))
        # r = int(np.random.laplace(0, num/eps))
        r = int(laplace.rvs(0, num/eps))
    x = lap_list[g][1] + (packets[i][1] - packets[g][1]) + r
    # print(g, i)
    if x > 1500:
        x = 1500
    if x < 0:
        x = 0

    n = [packets[i][0], x, packets[i][2]]
    return n, x - packets[i][1]


def dp_sel(ori_packets, eps, selected_idxes):

    buffer_q = queue.Queue()
    buffer_p = []  # [time, index, size]
    proc_q = queue.Queue()  # [buffered_time, buffered_index, size, cleaned_time, cleaned_index, real_n]
    return_q = queue.Queue()
    lap_overhead = 0
    n = [0,0,0]
    ori_packets = [n] + ori_packets
    lap_list = [n]

    while len(lap_list) != len(ori_packets):
        idx = len(lap_list)-2
        if idx not in selected_idxes:
            lap_list.append(ori_packets[idx+1])
        else:
            lap_p, diff_o = lap_csv(ori_packets, lap_list, eps)
            if lap_p[1] == 0:
                buffer_q.put([lap_p[0], len(lap_list) - 1, abs(diff_o)])
                # continue
            # else:
            lap_list.append(lap_p)

            real_n = 0
            a = buffer_q.qsize()
            b = proc_q.qsize()
            size_left = lap_p[1]
            size_use = 0

            if not buffer_q.empty() or buffer_p:
                while size_left > 0:
                    if buffer_p:
                        pass
                    else:
                        try:
                            buffer_p = buffer_q.get(False)
                        except queue.Empty:
                            break

                    if size_left > buffer_p[2]:
                        real_n += 1
                        proc_q.put(buffer_p + [lap_p[0], len(lap_list) - 2] + [real_n])
                        size_use += buffer_p[2]
                        size_left = size_left - buffer_p[2]
                        buffer_p = []
                        real_n = 0
                        try:
                            buffer_p = buffer_q.get(False)
                        except queue.Empty:
                            # buffer_p = []
                            if diff_o > 0:
                                if size_left >= diff_o:
                                    buffer_q.put([lap_p[0], len(lap_list) - 2, size_use])
                                    lap_overhead = lap_overhead + diff_o
                                else:
                                    buffer_q.put([lap_p[0], len(lap_list) - 2, lap_p[1] - diff_o])
                                    lap_overhead = lap_overhead + diff_o - size_left
                            else:
                                buffer_q.put([lap_p[0], len(lap_list) - 2, size_use + abs(diff_o)])
                            size_left = 0
                            break
                    else:
                        buffer_p[2] = buffer_p[2] - size_left
                        if size_left > diff_o > 0:
                            buffer_q.put([lap_p[0], len(lap_list) - 2, size_left - diff_o])
                        elif diff_o < 0:
                            buffer_q.put([lap_p[0], len(lap_list) - 2, size_left + abs(diff_o)])
                        real_n += 1
                        size_left = 0

            elif diff_o < 0:
                buffer_q.put([lap_p[0], len(lap_list) - 2, abs(diff_o)])
    left = 0
    while not buffer_q.empty():
        buffer_p = buffer_q.get(False)
        left = buffer_p[2] + left

    dum = int(left/1500)
    while dum > 0:
        lap_list.append([lap_list[-1][0]+0.000001, 1500, lap_list[-1][2]])
        left = left - 1500
        dum-=1
    lap_list.append([lap_list[-1][0]+0.000001, left, lap_list[-1][2]])

    return lap_list, proc_q, lap_overhead


def info_stat(eps, trace_name, ori_size, real_ap_overhead, et_ap_overhead, ap_overall_overhead, real_lap_overhead, et_lap_overhead, lap_overall_overhead, ori_end, overall_delay, unfinished):

    with open('stats/overhead_list_' + str(eps) + '.csv','a') as build:
        writer = csv.writer(build)
        writer.writerow([trace_name, ori_size, real_ap_overhead, et_ap_overhead, ap_overall_overhead,
                         real_lap_overhead, et_lap_overhead, lap_overall_overhead, ori_end, overall_delay, unfinished])


def main():
    csv_path = '/home/lhp/PycharmProjects/feature_analysis/datafiles/video/video_bin_numeric_padded.csv'
    folder = 'test'
    eps = 0.05
    score_path = '/home/lhp/PycharmProjects/feature_analysis/datafiles/mi_video_bin_py.csv'
    score_list = pd.read_csv(score_path)
    # score_list = score_list.values.tolist()
    # score_list.sort(key=su.sort_by_second)
    score_list = score_list.sort_values(by=['col1'], ascending=False)
    selected_indexes = score_list.iloc[:200,0]
    selected_indexes = selected_indexes.values.tolist()
    selected_indexes.sort()
    # csv_path = opts.csvPath
    # folder = opts.folder
    # eps = float(opts.eps)
    dp_dest = '/home/lhp/PycharmProjects/dataset/Video_dataset/sel_defense/dp/' + folder + '/'
    bf_dest = '/home/lhp/PycharmProjects/dataset/Video_dataset/sel_defense/buffer/' + folder + '/'
    if not os.path.isdir(dp_dest):
        os.makedirs(dp_dest)
    if not os.path.isdir(bf_dest):
        os.makedirs(bf_dest)
    packets = pd.read_csv(csv_path)
    packets = packets.values.tolist()
    pf = Path(csv_path)
    trace_name = pf.name[0:-4]

    # sel_packets = packets.iloc[selected_indexes, :].values.tolist()
    # outgoing = []
    for trace in packets:
        incoming = trace[1:]
        # for p in sel_packets:
        #     if p[2] == -1:
        #         incoming.append(p)
        #     else:
        #         outgoing.append(p)
        # packets = su.csv_numpy(csv_path)
        incoming_lap_list, incoming_proc_q, in_overhead = dp_bin(incoming, eps, selected_indexes)
        # outging_lap_list, outgoing_proc_q, out_overhead = dp_sel(outgoing, eps)
        # with open('test.csv','a') as ww:
        #     writer = csv.writer(ww)
        #     writer.writerow(incoming_lap_list)
        lap_list = trace[0] + incoming_lap_list

        buffer_list = list(incoming_proc_q.queue)
        buffer_list.sort(key=su.sort_by_name)
        buffer_list.append([in_overhead])
        # lap_list.sort(key=su.sort_by_name)

        lap_df = pd.DataFrame(lap_list)
        try:
            buffer_df = pd.DataFrame(buffer_list, columns = ['buffered_time', 'buffered_index', 'size', 'cleaned_time', 'cleaned_index', 'real_n'])
            buffer_df.to_csv(bf_dest + trace_name + 'buffer.csv', index=False)
        except AssertionError:
            print('no proc queue!!!')

        # lap_trace = pd.DataFrame(np.concatenate((packets.iloc[:start_idx,:].values, lap_df.iloc[2:,:].values, packets.iloc[end_idx:,:].values), axis=0))

        # packets.iloc[start_idx:start_idx+end_idx,:] = lap_df.iloc[2:2+end_idx,:].values
        # lap_trace.to_csv(dp_dest + trace_name + 'dp.csv', index=False)
        print(csv_path + ' is finished')


def parseOpts(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-pc','--csvPath', help='path to read csv files')
    parser.add_argument('-f','--folder', help='obf data folder')
    parser.add_argument('-eps','--eps', help='eps for laplase' )
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    # opts = parseOpts(sys.argv)
    main()
