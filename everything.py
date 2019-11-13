
import pandas as pd


if __name__ == '__main__':
    data = pd.read_csv('/home/lhp/PycharmProjects/dataset/Video_dataset/video_round1.csv',sep='delimiter', header=None)
    label = data.iloc[0,:]
    new = []
    for l in label.values:
        n = l[0:8]
        new.append(n)
    for idx, i in enumerate(new):
        data.iloc[0,idx] = i


