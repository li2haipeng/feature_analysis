from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection.mutual_info_ import _iterate_columns
from sklearn import preprocessing
import csv
import numpy as np
import pandas as pd
import pickle
from feast import MIFS


def mi_alexa():

    data = pd.read_csv('/home/lhp/PycharmProjects/dataset/Alexa_dataset/alexa_incoming.csv')
    x = data.iloc[:, 1:]
    le = preprocessing.LabelEncoder()
    labels = le.fit_transform(data.iloc[:,0])

    for c in _iterate_columns(x.values):
        c = c.reshape(-1,1)
        score = mutual_info_classif(c,labels)
        with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/mi_alexa_in.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(score)
    # score = mutual_info_classif(x, labels)
    # df = pd.DataFrame(score)
    # df.to_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/score_binary.csv',index=False)





def wf_preprc():

    x = []
    with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/X_train_NoDef.pkl', 'rb') as f:
        x1 = pickle.load(f, encoding='latin1')
    with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/X_test_NoDef.pkl', 'rb') as f:
        x2 = pickle.load(f, encoding='latin1')
    with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/X_valid_NoDef.pkl', 'rb') as f:
        x3 = pickle.load(f, encoding='latin1')
    x = x1 + x2 + x3

    # x = np.array(x)
    # x = x.ravel()
    # x = x.tolist()
    # xdf = pd.DataFrame(x)


    with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/y_train_NoDef.pkl', 'rb') as f:
        y1 = pickle.load(f, encoding='latin1')
    with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/y_test_NoDef.pkl', 'rb') as f:
        y2 = pickle.load(f, encoding='latin1')
    with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/y_valid_NoDef.pkl', 'rb') as f:
        y3 = pickle.load(f, encoding='latin1')

    y = y1 + y2 + y3
    y = np.array(y)
    y = y.ravel()
    y = y.tolist()
    for i,p in enumerate(x):
        a = np.append(y[i], p)
        with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/wf.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(a)
    # df = pd.DataFrame(y)
    # # df = pd.concat([xdf, df], axis=1, sort=False)
    # df.to_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/ori/WF.csv',index=False, header=False)

    # for p in y:
    #     with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/y_wf.csv', 'a') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(p)



def mi_wf():
    wf_preprc()
    x = []
    chunk_l = []

    chunksize = 2000
    for chunk in pd.read_csv('feature_analysis/datafiles/X_wf.csv', chunksize=chunksize, header=None):
        chunk_l.append(chunk)
        print(len(chunk_l))

    for i in range(5000):
        for chunk in chunk_l:
            x = np.append(x, chunk.iloc[:, i].values)
        x = x.reshape(-1,1)

        score = mutual_info_classif(x, y)
        x = []
        with open('feature_analysis/datafiles/score_wf.csv', 'a') as s:
            writer = csv.writer(s)
            writer.writerow(score)


def mi_video():
    data = pd.read_csv('/home/lhp/PycharmProjects/dataset/Video_dataset/video_bin_numeric_padded.csv', header=None)
    x = data.iloc[:, 1:]
    le = preprocessing.LabelEncoder()
    labels = le.fit_transform(data.iloc[:, 0])

    for c in _iterate_columns(x.values):
        c = c.reshape(-1, 1)
        score = mutual_info_classif(c, labels)
        with open('/home/lhp/PycharmProjects/feature_analysis/datafiles/mi_video_bin_py.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(score)

def main():

    mi_wf()
    # mi_alexa()
    # mi_video()

if __name__ == '__main__':
    main()