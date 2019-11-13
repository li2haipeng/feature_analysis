import sys
from sklearn import preprocessing
import pandas as pd
import numpy as np
from pyitlib import discrete_random_variable as drv
import datetime



def _jmi(feature_set, labels, score_list):
    ###
    # I(x,y;c) = H(x,c) - H(c) - [ H(x,c,y) - H(c,y) ] + I(y;c) #
    ####
    results=[]
    col = list(feature_set)
    labels = np.reshape(labels, (1, -1))
    for i in col:
        candidate_f = feature_set[i]
        candidate_f = np.reshape(candidate_f.values, (1, -1))
        print(i+ ' start at ' + str(datetime.datetime.now()))
        for j in range(int(i)+1, 400):
            sf = feature_set[str(j)]
            sf = np.reshape(sf.values, (1,-1))

            I_yc = score_list.iloc[j, 0]
            H_x_c = drv.entropy_conditional(candidate_f, labels)

            xcy = np.append([candidate_f, labels], [sf], axis=0)
            H_xcy = drv.entropy_joint(xcy)

            # cy = np.append([labels], [sf], axis=0)
            cy = np.concatenate((labels, sf))
            cy = np.reshape(cy,(-1,2))
            H_cy = drv.entropy_joint(cy)

            I_xy_c = float(H_x_c - (H_xcy - H_cy) + I_yc)
            results.append([[i,j], I_xy_c])

            if I_xy_c < 0:
                print()

            results.append([[i,j], I_xy_c])
            df = pd.DataFrame(results)
            df.to_csv('jmi_2packets.csv')
        print('end at ' + str(datetime.datetime.now()))
    df = pd.DataFrame(results)
    df.to_csv('jmi_2packets.csv')


if __name__ == '__main__':
    # num_to_select = int(sys.argv[1])
    data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/wf.csv')
    # data = su.csv_numpy('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/wf.csv')
    x = data.iloc[:, 1:]
    le = preprocessing.LabelEncoder()
    labels = le.fit_transform(data.iloc[:, 0])

    max_mi = 0
    max_index = 0
    score_list = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/WF_dataset/score_wf.csv')

    _jmi(x,  labels, score_list)

    print('Done at ' + str(datetime.datetime.now()))

    print()
