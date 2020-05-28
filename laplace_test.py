from __future__ import division
import sys
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


def dp_bin(ori_packets, eps_light, eps_heavy, selected_idxes):

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
        lap_p = 0
        if (idx+1) not in selected_idxes:
            lap_p, diff_o = lap_trace(ori_packets, lap_list, eps_light)
            lap_overhead+= diff_o
        else:
            lap_p, diff_o = lap_trace(ori_packets, lap_list, eps_heavy)
            lap_overhead+= diff_o
                # continue
            # else:
        lap_list.append(lap_p)


    return lap_list, proc_q, lap_overhead


def main():

    b = float(sys.argv[1])
    r = int(sys.argv[2])
    eps_heavy = float(sys.argv[3])
    eps_light = 0.000005

    # method = 'mi'
    # b = 0.25
    # r = 720
    # eps_heavy = 0.000005
    # eps_light = 0.000005


    l = int(180/b)
    csv_path = 'datafiles/video/video_bin_'+ str(b) +'.csv'
    packets = pd.read_csv(csv_path)
    packets = packets.values.tolist()

    selected_indexes = [i for i in range(120,120+r)]
    # selected_indexes.sort()
    s = 0
    overhead = 0
    ori_size = 0
    for trace in packets:
        incoming = trace[1:]
        s+=1
        idx = s%200
        incoming_lap_list, incoming_proc_q, in_overhead = dp_bin(incoming, eps_light, eps_heavy, selected_indexes)
        incoming_lap_list[0] = trace[1]
        lap_list = incoming_lap_list
        with open('/home/lhp/Documents/pfi_'  + str(b) + '_test_' + str(r) + '_' + str(eps_heavy) +'_' + str(eps_light) +'.csv', 'a') as w:
            writer = csv.writer(w)
            writer.writerow(lap_list)
        overhead += in_overhead
        ori_size += sum(incoming)

        if s%200 == 0:
            print(str(int(s)) + ' ' + str(b) + ' ' +str(selected_indexes[-1]) + ' ' + str(eps_heavy) + ' is finished')
    # with open('overhead_selected/' + str(b) +'overhead_' + str(r) + '_' +  method + '_' + str(eps) + '.csv', 'a') as w:

    with open('pfi_weighted_overhead_test.csv', 'a') as w:
        writer = csv.writer(w)
        writer.writerow([b, r, eps_heavy, eps_light, ori_size, overhead])


if __name__ == "__main__":
    main()
