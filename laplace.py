from __future__ import division
import sys
sys.path.append('/home/lhp/PycharmProjects/feature_analysis/')
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


def info_stat(eps, trace_name, ori_size, real_ap_overhead, et_ap_overhead, ap_overall_overhead, real_lap_overhead, et_lap_overhead, lap_overall_overhead, ori_end, overall_delay, unfinished):

    with open('stats/overhead_list_' + str(eps) + '.csv','a') as build:
        writer = csv.writer(build)
        writer.writerow([trace_name, ori_size, real_ap_overhead, et_ap_overhead, ap_overall_overhead,
                         real_lap_overhead, et_lap_overhead, lap_overall_overhead, ori_end, overall_delay, unfinished])


def lap_trace(packets, lap_list, eps):
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
    x = lap_list[g] + (packets[i] - packets[g]) + r
    # print(g, i)
    # if x > 1500:
    #     x = 1500
    if x < 0:
        x = 0

    n = x
    return n, x - packets[i]


def dp_bin(ori_packets, eps, selected_idxes):

    buffer_q = queue.Queue()
    buffer_p = []  # [time, index, size]
    proc_q = queue.Queue()  # [buffered_time, buffered_index, size, cleaned_time, cleaned_index, real_n]
    return_q = queue.Queue()
    lap_overhead = 0
    n = 0
    ori_packets = [n] + ori_packets
    lap_list = [n]

    while len(lap_list) != len(ori_packets):
        idx = len(lap_list)
        if idx not in selected_idxes:
            lap_list.append(ori_packets[idx])
        else:
            lap_p, diff_o = lap_trace(ori_packets, lap_list, eps)
            if lap_p == 0:
                buffer_q.put([lap_p, len(lap_list) - 1, abs(diff_o)])
                # continue
            # else:
            lap_list.append(lap_p)

            real_n = 0
            a = buffer_q.qsize()
            b = proc_q.qsize()
            size_left = lap_p
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
                        proc_q.put(buffer_p + [lap_p, len(lap_list) - 2] + [real_n])
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
                                    buffer_q.put([lap_p, len(lap_list) - 2, size_use])
                                    lap_overhead = lap_overhead + diff_o
                                else:
                                    buffer_q.put([lap_p, len(lap_list) - 2, lap_p - diff_o])
                                    lap_overhead = lap_overhead + diff_o - size_left
                            else:
                                buffer_q.put([lap_p, len(lap_list) - 2, size_use + abs(diff_o)])
                            size_left = 0
                            break
                    else:
                        buffer_p[2] = buffer_p[2] - size_left
                        if size_left > diff_o > 0:
                            buffer_q.put([lap_p, len(lap_list) - 2, size_left - diff_o])
                        elif diff_o < 0:
                            buffer_q.put([lap_p, len(lap_list) - 2, size_left + abs(diff_o)])
                        real_n += 1
                        size_left = 0

            elif diff_o < 0:
                buffer_q.put([lap_p, len(lap_list) - 2, abs(diff_o)])
    left = 0
    while not buffer_q.empty():
        buffer_p = buffer_q.get(False)
        left = buffer_p[2] + left

    dum = int(left/1000000000)
    while dum > 0:
        lap_list.append(1000000000)
        left = left - 1000000000
        dum-=1
    lap_list.append(left)

    return lap_list, proc_q, lap_overhead


def main():
    csv_path = '/home/lhp/PycharmProjects/feature_analysis/datafiles/video/video_bin_numeric_padded.csv'
    packets = pd.read_csv(csv_path)
    packets = packets.values.tolist()
    eps = 0.0000005

    score_path = '/home/lhp/PycharmProjects/feature_analysis/datafiles/mi_video_bin_py.csv'
    score_list = pd.read_csv(score_path)
    score_list = score_list.sort_values(by=['col1'], ascending=False)
    selected_indexes = score_list.iloc[:30,0]
    selected_indexes = selected_indexes.values.tolist()
    selected_indexes.sort()
    s= 0
    for trace in packets:
        incoming = trace[1:]
        s+=1
        idx = s%200
        incoming_lap_list, incoming_proc_q, in_overhead = dp_bin(incoming, eps, selected_indexes)
        incoming_lap_list[0] = trace[0]
        lap_list = incoming_lap_list
        with open('video_bin_dp_5e-6_30.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(lap_list)

        buffer_list = list(incoming_proc_q.queue)
        buffer_list.sort(key=su.sort_by_name)
        buffer_list.append([in_overhead])

        bf_dest = '/home/lhp/PycharmProjects/dataset/Video_dataset/sel_defense/buffer/' + str(int(trace[0])) + '/'
        if not os.path.isdir(bf_dest):
            os.makedirs(bf_dest)
        # try:
        #     buffer_df = pd.DataFrame(buffer_list, columns = ['buffered_time', 'buffered_index', 'size', 'cleaned_time', 'cleaned_index', 'real_n'])
        #     buffer_df.to_csv(bf_dest + str(int(trace[0])) + '_' + str(int(idx)) + '_buffer.csv', index=False)
        # except AssertionError:
        #     print('no proc queue!!!')

        if s%200 == 0:
            print(str(int(s)) + ' is finished')


if __name__ == "__main__":
    main()
