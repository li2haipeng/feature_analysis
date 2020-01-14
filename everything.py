from __future__ import division
import csv
import pandas as pd
import random



if __name__ == '__main__':
    a = 0.00005
    a = str(a)
    b = len(a)
    path = 'wf_decoy.csv'
    chunksize = 5000
    count = 0
    dis = {500:0,
           1000:0,
           1500:0,
           2000:0,
           2500:0,
           3000:0,
           3500:0,
           4000:0,
           4500:0,
           6000:0}
    for chunk in pd.read_csv(path, chunksize=chunksize):
        # count += 1
        # chunk.to_csv(str(count)+'.csv',header=False,index=None)
        # print(chunk.shape)
        a = chunk.astype(bool).sum(axis=1)
        for i in a:
            for k,v in dis.items():
                if i <= k:
                    dis[k] += 1
                    # break
        print()
    for k,v in dis.items():
        dis[k] = v/95000
    with open('len_info_decoy.csv', 'a') as w:
        writer = csv.DictWriter(w, dis.keys())
        writer.writeheader()
        writer.writerow(dis)