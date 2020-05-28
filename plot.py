import pandas as pd
import os
import sys
import csv
import collections
from pylab import *
import matplotlib.font_manager
import matplotlib
import selfUtils as su
from matplotlib import rc
# import matplotlib.pyplot as plt


def df_dict(df):

    dic = {}
    k = df.keys().values
    v = df.values
    for i in range(len(k)):
        dic[k[i]] = v[0][i]
    return dic


def bar_fig(x, y, n_g):

    n_groups = n_g

    # create plot
    fig, ax = plt.subplots(figsize = (8.75, 1.75))
    index = np.arange(n_groups)
    bar_width = 1
    opacity = 0.2
    for yy in y:

        label = yy[0]
        data = yy[1:]
        r = plt.bar(index, data, bar_width,
                         alpha=opacity,
                         color='black')

    # rects2 = plt.bar(index + bar_width, y1, bar_width,
    #                  alpha=opacity,
    #                  color='g',
    #                  label='0.5')
    #
    # rects3 = plt.bar(index + 2* bar_width, y2, bar_width,
    #                  alpha=opacity,
    #                  color='black',
    #                  label='5.0')



    plt.xlabel('time', fontsize=16)
    # plt.ylabel('pdf',fontsize=16)
    # plt.title('PDF of buffer cleaning latency')
    plt.xticks(index + 0.5*bar_width, [])

    plt.yticks([])
    plt.axis('off')
    # plt.legend()
    plt.tight_layout()
    savefig('time_slot.pdf', format='pdf')
    plt.show()
    exit(0)


def fig_order(x, y, y1): ## name, x, y, x_lim, y_lim, x_step, y_step, x_lable


    matplotlib.rcParams['ps.useafm'] = True
    matplotlib.rcParams['pdf.use14corefonts'] = True

    # matplotlib.rcParams['text.usetex'] = True
    # Set appropriate figure width/height

    fig = plt.figure(figsize=(5.75, 3.75))

    # Set appropriate margins, these values are normalized into the range [0, 1]

    subplots_adjust(left=0.20, bottom=0.20, right=0.90, top=0.90, wspace=0.1, hspace=0.1)


    # Plot lines in the figure

    ax = fig.add_subplot(111)
    ax.plot(x, y, marker ='^',  markersize = 10, markeredgewidth=2.4, markerfacecolor='none', linewidth=2.4, color='red', label='Our CNN')
    ax.plot(x, y1, marker ='o', markersize = 10, markeredgewidth=2.4,markerfacecolor='none', linewidth=2.4, color='green',label='USENIX17')




    prop = matplotlib.font_manager.FontProperties(size=12)

    leg = legend(loc='upper right', prop=prop)
    # set the fontsize of the legend
    for t in leg.get_texts():
       t.set_fontsize('16')

    # set ticker
    majorLocator_x = MultipleLocator(1)
    majorLocator_y = MultipleLocator(0.1)
    # ax.xaxis.set_major_locator(majorLocator_x)
    ax.yaxis.set_major_locator(majorLocator_y)

    # Set labels for axes

    ax.tick_params(labelsize=18)
    ax.set_ylim(0.5, 1.0)

    # xlim(0, 15)
    xlabel('Interval Size w (second)', fontsize=18)
    ax.set_ylabel('Attack Accuracy', fontsize=18)

    # Save file as .eps

    savefig('acc.pdf', format='pdf')
    show()
    exit(0)


def latency_plot():

    x= ["0.05", '0.25', '0.5', '1', '2']
    y = [0.92, 0.90, 0.82, 0.80, 0.76] #mi2
    y1 = [0.75, 0.80, 0.80, 0.79, 0.79]

    # y = [0.44, 0.23, 0.02, 0.01]#mi0.25
    # y1 = [0.45, 0.29, 0.04, 0.01]
    #
    # y = [0.65, 0.57, 0.02, 0.01]#jmim2
    # y1 = [0.70, 0.61, 0.04, 0.01]
    # #
    # y = [0.46, 0.29, 0.02, 0.01]#jmim0.25
    # y1 = [0.66, 0.46, 0.04, 0.01]
    # y = [0.01, 0.01, 0.08, 0.67, 0.72, 0.70]#jmim0.25
    # y1 = [0.01, 0.01, 0.011, 0.69, 0.70, 0.72]

    # y = [245.4, 357.2, 528.9, 705.0]#jmim0.25
    # y = [94.8, 189.2, 283.5, 377.9]
    # y1 = [18.2, 35.5, 52.9, 70.2]  # jmim0.25
    # y1 = [9.2, 18.4, 27.6, 36.7]
    # y = [91.4, 89.7, 81.8, 79.0, 75.5]
    fig_order(x, y, y1)
    # x = [i for i in range(1)]
    # y = []
    # for m in ['mrmr', 'jmim', 'mi']:
    #     for w in ['0.05', '0.25', '0.5', '1.0', '2.0']:
    #         path ='sel' + '/' + m + '_' + w + '.csv'
    #         data = pd.read_csv(path)['0'].values.tolist()
    #         y.append([m + '_' + w] +data)
    #
    # bar_fig(x, y,180)
def pfi_plot():
    print()

def main():


    latency_plot()
    pfi_plot()
######################################################Distirbution Figure Generator#############################################################################################

    in_interval = pd.read_csv('stats/distribution_gamma/adapt_in_distribution_interval.csv')
    in_size = pd.read_csv('stats/distribution_gamma/adapt_in_distribution_size.csv')
    out_interval = pd.read_csv('stats/distribution_gamma/adapt_out_distribution_interval.csv')
    out_size = pd.read_csv('stats/distribution_gamma/adapt_out_distribution_size.csv')

    # in_interval_l, in_size_l, out_interval_l, out_size_l = map(lambda l: l.values.tolist(), [in_interval, in_size, out_interval, out_size])

    in_interval_l, in_size_l, out_interval_l, out_size_l = map(su.csv_numpy,
                                                               ['stats/distribution_gamma/in_interval_r.csv', 'stats/distribution_gamma/in_size_r.csv',
                                                                'stats/distribution_gamma/out_interval_r.csv', 'stats/distribution_gamma/out_size_r.csv'])

    # x = [str(p[0]) for p in out_interval_l]
    x=[]
    for p in in_size_l:
        if p[0] < 1:
            x.append(str(p[0]))
        else:
            x.append(str(int(p[0])))
    y = [p[1] for p in in_size_l][0:10]



    # create plot
    fig, ax = plt.subplots(figsize=(7.75, 3.75))
    index = np.arange(10)
    bar_width = 0.5
    opacity = 0.8

    rects1 = plt.bar(index + bar_width, y, bar_width,
                     alpha=opacity,
                     color='blue')


    # plt.xlabel('Packet inter-arrival time (ms)', fontsize=16)
    plt.xlabel('Packet size (byte)', fontsize=16)
    plt.ylabel('PDF', fontsize=16)
    # plt.title('PDF of buffer cleaning latency')
    plt.xticks(index + bar_width, x[0:10])
    ax.tick_params(labelsize = 16)


    majorLocator_y = MultipleLocator(0.1)
    ax.yaxis.set_major_locator(majorLocator_y)

    # Set labels for axes

    ax.tick_params(labelsize=16)
    ax.set_ylim(0, 0.7)

    plt.tight_layout()
    savefig('in_size.pdf', format='pdf')
    plt.show()
    exit(0)


if __name__ == '__main__':
    main()
