import pandas as pd
import sys
import selfUtils as su


def jaccard(a, b):
    c = a.intersection(b)
    j = 0
    if len(c) != 0:
        j = float(len(c)) / (len(a) + len(b) - len(c))
    return j


def neighors(f_list, w):
    # for i, p in enumerate(f_list):
    #     if i == len(f_list)-1:
    #         continue
    #     if f_list[i+1] - p > w:
    #         a = [n for n in range(p, p+w)]
    #         f_list.extend(a)
    #     else:
    #         a = [n for n in range()]
    ff_list = []
    for i, p in enumerate(f_list):
        # print(i)
        a = [n for n in range(p-w, p+w)]
        ff_list.extend(a)
    return_list = []
    for p in ff_list:
        if p not in return_list:
            return_list.append(p)
    return return_list


if __name__ == "__main__":
    # b = 0.05
    b = float(sys.argv[1])

    w = int(0.25/b)
    w = 2
    # method = 'mrmr'
    method = sys.argv[2]

    mi = pd.read_csv('results/KB/mi/mi_video_bin_'+ str(b) +'_kb.csv', header=None)
    mi = mi.sort_values(mi.columns[1], ascending=False)
    jmim = pd.read_csv('results/KB/jmim/jmim_video_bin_'+ str(b) +'_kb.csv', header=None)
    s = len(mi)*0.1
    k = int(s)
    mi_k = mi.iloc[0:k,0].values.tolist()
    # mi_k.sort(key=su.sort_by_name)
    mi_kk = neighors(mi_k, w)

    jmim_k = jmim.iloc[0:k,0].values.tolist()
    # jmim_k.sort(key=su.sort_by_name)
    jmim_kk = neighors(jmim_k, w)
    selected = pd.read_csv('results/KB/' + method + '/' + method + '_video_bin_'+ str(b) +'_kb.csv', header=None)

    # data1 = data1.sort_values(data1.columns[1], ascending=False)

    selected = selected.iloc[0:k, 0].values.tolist()
    selected_kk = neighors(selected,w)
    # selected.sort(key=su.sort_by_name)
    x1 = set(jmim_kk)
    x2 = set(selected_kk)
    j = jaccard(x1, x2)
    # print(x1)
    # print(x2)
    f = open("jaccard_result_nn.txt", "a+")
    f.write(str(b) + ' ' +  method + ' with jmim'+ ' ' + str(j)+ ' ' + str(len(selected_kk))+ ' ' + str(len(mi_kk)) + '\n')
    f.close()
    print(str(b) + ' ' + method + ' with jmim'+ ' ' + str(j))
