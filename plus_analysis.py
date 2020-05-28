import pandas as pd
import os
import sys
import csv

def acc_collect():
    path = '/home/lhp/Documents/acc_result'
    files = os.listdir(path)
    for f_name in files:
        data = f_name.split("_")
        method = data[0]
        r = data[1]
        heavy_eps = data[2]
        light_eps = data[3]
        bin = data[8]
        acc = data[9][0:-3]
        result = [method, bin, r, heavy_eps, light_eps, acc]
        with open('acc_result.csv', 'a+') as ff:
            writer = csv.writer(ff)
            writer.writerow(result)


# def plus_distance():
#     bb = float(sys.argv[1])
#     # bb = 0.25
#     data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/results/KB/jmi_plus/jmi_plus_video_bin_' + str(bb) + '_kb.csv',header=None)
#     _range = [0, 99]
#
#     d = 5
#     block = int(len(data)/100) - 100
#     sum_a = sum_b = ave_a = ave_b = la = lb = 0
#     a=b=[]
#     for i in range(0, block):
#         idx = data.iloc[_range[0] + i*100 - 1:_range[0]+d+ i*100 - 1, 0].values.tolist()
#
#         a = data.iloc[_range[0]+ i*100 - 1:_range[0]+d+ i*100 - 1, 1].values.tolist()
#         b = data.iloc[_range[1]-d+ i*100 - 1:_range[1]+ i*100 - 1, 1].values.tolist()
#         sum_a += sum(a) -sum(idx)
#         sum_b += sum(b) - sum(idx)
#         la += len(a)
#         lb += len(b)
#     try:
#         ave_a = (sum_a/block)/la
#         ave_b = (sum_b/block)/lb
#     except:
#         ave_a = ave_b = 0
#     f = open("plus_analysis.txt", "a+")
#     f.write(str(bb) + ' ' + 'jmi' +  ' ' + str(ave_a) + ' ' + str(ave_b) + '\n')
#     f.close()

def plus_distance():
    bb = float(sys.argv[1])
    # bb = 0.25
    data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/results/KB/mi_plus/mi_plus_video_bin_' + str(bb) + '_kb.csv')
    l = int(180/0.25)
    block = int(l*0.1)
    sum_a = sum_b = ave_a = ave_b = 0
    for i in range(l):
        section = data.loc[data['idx'] == i+1]['a'].loc[:block-1]
        top = section.loc[:int(block*0.1)].tolist()
        bottom = section.iloc[-int(block*0.1):].tolist()
        sum_a += sum(top) - len(top) * (i+1)
        sum_b += sum(bottom) -  len(top) * (i+1)
        ave_a += sum_a/(block*0.1)
        ave_b += sum_b / (block * 0.1)
    a = ave_a/l * bb
    b = ave_b/l * bb

    f = open("plus_analysis.txt", "a+")
    f.write(str(bb) + ' ' + 'mi' +  ' ' + str(a) + ' ' + str(b) + '\n')
    f.close()

if __name__ == '__main__':
    plus_distance()

