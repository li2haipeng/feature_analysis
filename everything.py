from __future__ import division
import csv
import pandas as pd
import random



if __name__ == '__main__':

    path = '/home/lhp/PycharmProjects/feature_analysis/wf_decoy.csv'
    chunksize = 1000
    count = 0
    for chunk in pd.read_csv(path, chunksize=chunksize, names=list(range(5000))):
        # count += 1
        # chunk.to_csv(str(count)+'.csv',header=False,index=None)
        print(chunk.shape)
