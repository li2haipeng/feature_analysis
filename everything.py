from __future__ import division
import csv
import pandas as pd
import random


def aa():
    a = 0.00005
    a = str(a)
    b = len(a)
    path = 'wf_decoy.csv'
    chunksize = 5000
    count = 0
    dis = {500: 0,
           1000: 0,
           1500: 0,
           2000: 0,
           2500: 0,
           3000: 0,
           3500: 0,
           4000: 0,
           4500: 0,
           6000: 0}
    for chunk in pd.read_csv(path, chunksize=chunksize):
        # count += 1
        # chunk.to_csv(str(count)+'.csv',header=False,index=None)
        # print(chunk.shape)
        a = chunk.astype(bool).sum(axis=1)
        for i in a:
            for k, v in dis.items():
                if i <= k:
                    dis[k] += 1
                    # break
        print()
    for k, v in dis.items():
        dis[k] = v / 95000
    with open('len_info_decoy.csv', 'a') as w:
        writer = csv.DictWriter(w, dis.keys())
        writer.writeheader()
        writer.writerow(dis)


def f():

    for m in ['mrmr', 'jmim']:
        for w in ['0.05', '0.25', '0.5', '1.0', '2.0']:
            path ='results/KB/' + m + '/' + m + '_video_bin_' + w + '_kb.csv'
            data = pd.read_csv(path, header=None)
            sel = (data.iloc[:, 0] * float(w)).tolist()
            sel.sort()
            sel = [round(i) for i in sel]
            e = []
            for i in range(180):
                if i in sel:
                    e.append(1)
                else:
                    e.append(0)
            # d = pd.DataFrame(sel)
            # d.to_csv('sel/' + m + '_' + w + '.csv', index=False)
            dd = pd.DataFrame(e)
            dd.to_csv('sel/' + m + '_' + w + '.csv', index=False)



if __name__ == '__main__':
    # f()
    for w in ['0.05', '0.25', '0.5', '1.0', '2.0']:
        path = 'results/KB/mi/mi_video_bin_' + w + '_kb.csv'
        data = pd.read_csv(path, header=None)
        data = data.sort_values(data.columns[1], ascending=False)
        b = int(180/float(w)*0.1)
        sel = (data.iloc[0:b, 0] * float(w)).tolist()
        sel.sort()
        sel = [round(i) for i in sel]
        e = []
        for i in range(180):
            if i in sel:
                e.append(1)
            else:
                e.append(0)
        # d = pd.DataFrame(sel)
        # d.to_csv('sel/' + m + '_' + w + '.csv', index=False)
        dd = pd.DataFrame(e)
        dd.to_csv('sel/mi' + '_' + w + '.csv', index=False)