import pandas as pd
import sys


def jaccard(a, b):
    c = a.intersection(b)
    j = 0
    if len(c) != 0:
        j = float(len(c)) / (len(a) + len(b) - len(c))
    return j


if __name__ == "__main__":
    # b = 0.05
    b = float(sys.argv[1])
    r = int(sys.argv[2])/10

    # method = 'mrmr'
    method = sys.argv[3]

    mi = pd.read_csv('results/KB/mi/mi_video_bin_'+ str(b) +'_kb.csv', header=None)
    mi = mi.sort_values(mi.columns[1], ascending=False)
    s = len(mi)*0.1
    k = int(r * s / b)
    mi_k = mi.iloc[0:k,0].values.tolist()
    selected = pd.read_csv('results/KB/' + method + '/' + method + '_video_bin_'+ str(b) +'_kb.csv', header=None)
    # data1 = data1.sort_values(data1.columns[1], ascending=False)

    selected = selected.iloc[0:k, 0].values.tolist()
    x1 = set(mi_k)
    x2 = set(selected)
    j = jaccard(x1, x2)
    # print(x1)
    # print(x2)
    f = open("jaccard_result.txt", "a+")
    f.write(str(b) + ' ' + str(r) + ' ' + method + ' with mi'+ ' ' + str(j) + '\n')
    f.close()
    print(str(b) + ' ' + str(r) + ' ' + method + ' with mi'+ ' ' + str(j))
