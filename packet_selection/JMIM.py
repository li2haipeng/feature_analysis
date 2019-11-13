from sklearn import preprocessing
import pandas as pd
import numpy as np
from pyitlib import discrete_random_variable as drv
import datetime
import sys


def _jmim(selected_feature, feature_set, num_to_select, labels, score_list):
    ###
    # I(x,y;c) = H(x|c) - [ H(x,c,y) - H(c,y) ] + I(y;c) #
    ####

    col = list(feature_set)
    pool = []
    for i in col:
        candidate_f = feature_set[i]
        candidate_f = np.reshape(candidate_f.values, (1, -1))
        min_jmi = 1000000000
        min_feature = []
        index = 0
        I_xy_c = 0
        for sf_packge in selected_feature:
            # print('round start at ' + str(datetime.datetime.now()))
            sf = sf_packge[1]
            sf_idx = sf_packge[0]

            I_yc = score_list.iloc[sf_idx, 0]

            sf = np.reshape(sf, (1,-1))
            labels = np.reshape(labels, (1, -1))
            H_c = drv.entropy(labels)
            H_x_c = drv.entropy_conditional(candidate_f, labels)

            xcy = np.append([candidate_f, labels], [sf], axis=0)
            H_xcy = drv.entropy_joint(xcy)

            cy = np.append([labels], [sf], axis=0)
            H_cy = drv.entropy_joint(cy)
            H_y_c = drv.entropy_conditional(sf, labels)

            H_cy2 = H_y_c + H_c

            I_xy_c = H_x_c - (H_xcy - H_cy) + I_yc


            labels = np.reshape(labels, (-1, 1))
            if I_xy_c < min_jmi:
                min_jmi = I_xy_c
                min_feature = candidate_f
                index = int(i)
        print(I_xy_c)
        if I_xy_c < 0:
            print()
        pool.append([index, min_feature, min_jmi])
        # print('round end at ' + str(datetime.datetime.now()))

    max_candidate_score = 0
    max_candidate_idx = 0
    max_candidate = []
    for candidate in pool:
        if float(candidate[2]) > max_candidate_score:
            max_candidate = candidate[1]
            max_candidate_idx = candidate[0]
            max_candidate_score = float(candidate[2])

    selected_feature.append([max_candidate_idx, max_candidate, max_candidate_score])
    feature_set.drop(columns=[str(max_candidate_idx)], inplace=True)


    print(str(len(selected_feature)) + ' ' + str(max_candidate_idx) + ' ' + str(max_candidate_score) + ' at ' + str(datetime.datetime.now()))

    return selected_feature, feature_set


if __name__ == '__main__':

    # num_to_select = int(sys.argv[1])
    num_to_select = 150
    data = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/alexa/generic_class.csv')
    x = data.iloc[:, 1:]
    le = preprocessing.LabelEncoder()
    labels = le.fit_transform(data.iloc[:, 0])

    max_mi = 0
    max_index = 0
    score_list = pd.read_csv('/home/lhp/PycharmProjects/feature_analysis/datafiles/alexa/scores/alexa_mi.csv')

    for idx, s in score_list.iterrows():
        if s['0'] > max_mi:
            max_mi = s['0']
            max_index = idx
    max_feature = list(x[str(max_index)])
    x.drop(columns=[str(max_index)],inplace=True)
    selected_feature = [[max_index, max_feature, max_mi]]
    print('Start to select '+ str(num_to_select) + ' features at ' + str(datetime.datetime.now()))
    print('number ' + 'index ' + 'score ' + ' time')

    while len(selected_feature) < num_to_select:
        (selected_feature, feature_set) = _jmim(selected_feature, x, num_to_select, labels, score_list)
        print('fs.shape = ' + str(feature_set.shape))

    print('Done at ' + str(datetime.datetime.now()))
    df = pd.DataFrame(selected_feature)
    df = df.iloc[:, [0, 2]]
    df.to_csv('jmim.csv', index=False)


    print()
