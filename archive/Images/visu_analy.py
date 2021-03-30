import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.stats as scp
import numpy as np
import pandas as pd
from pylab import rcParams
mpl.style.use("default")

def position_distri ():
    no_ice = [1726.00,1725.00,1716.00,1570.00,1238.00,1015.00,815.00,719.00,694.00,424.00,188.00,136.00,117.00,75.00,52.00,39.00,38.00,30.00,24.00,17.00,13.00,12.00,6.00,6.00,5.00]
    ice = [71.00,185.00,44.00,42.00,335.00,86.00,12.00,160.00,12.00,3.00,6.00,10.00,6.00,1.00,5.00,0.00,5.00,0.00,2.00,0.00,0.00,0.00,0.00,0.00,0.00]
    no_ice = no_ice[:20]
    ice = ice[:20]
    labels = [str(x).zfill(1) for x in range(20)]

    x = np.arange(len(labels))  # the label locations
    width = 0.4  # the width of the bars

    fig, ax = plt.subplots()
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray", linestyle="dashed")
    ax.bar(x + width / 2, ice, width, label='Ice ring',  color="steelblue", edgecolor="black")
    ax.bar(x - width / 2, no_ice, width, label='Non ice ring', color="darkseagreen", edgecolor="black")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Amount')
    ax.set_title('Ice ring contamination by position index')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    plt.savefig("/Users/kristophernolte/Documents/Helcaraxe_v2/stats/position_distr.svg")
    plt.show()

def stacked_bar():
    no_ice = np.asarray([1726.00, 1725.00, 1716.00, 1570.00, 1238.00, 1015.00, 815.00, 719.00, 694.00, 424.00, 188.00, 136.00,
              117.00, 75.00, 52.00, 39.00, 38.00, 30.00, 24.00, 17.00, 13.00, 12.00, 6.00, 6.00, 5.00])
    ice = np.asarray([71.00, 185.00, 44.00, 42.00, 335.00, 86.00, 12.00, 160.00, 12.00, 3.00, 6.00, 10.00, 6.00, 1.00, 5.00, 0.00,
           5.00, 0.00, 2.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00])

    xrange = 11
    xlabels = ['3.95-\n3.81',
     '3.75-\n3.58',
     '3.48-\n3.37',
     '2.69-\n2.64',
     '2.30-\n2.21',
     '2.09-\n2.04',
     '1.95-\n1.94',
     '1.94-\n1.89',
     '1.89-\n1.86',
     '1.72-\n1.71',
     '1.53-\n1.52',
     '1.48-\n1.47',
     '1.45-\n1.43',
     '1.37-\n1.36',
     '1.31-\n1.29',
     '1.29-\n1.25']

    xlabels = xlabels[:xrange]
    no_ice = no_ice - ice
    no_ice = no_ice[:xrange]
    ice = ice[:xrange]
    labels = [str(x).zfill(1) for x in range(xrange)]
    x = np.arange(len(labels))
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 5)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray", linestyle="dashed")

    width =  np.asarray([0.146,0.172,0.111,0.057,0.085,0.053,0.015,0.038,0.027,0.011,0.011])*3.5+0.15 # the width of the bars: can also be len(x) sequence

    ax.bar(labels, no_ice, width, color="darkseagreen", edgecolor="black", label="non ice ring")
    ax.bar(labels, ice, width, bottom=no_ice, color="steelblue", edgecolor="black", label="ice ring")

    ax.set_ylabel('Amount')
    ax.set_title('Ice ring contamination by position index')
    ax.set_xticks(x)
    ax.set_xlabel("[Å]")
    ax.set_xticklabels(xlabels)
    plt.legend()

    plt.savefig("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/stats/position_distr.svg")
    plt.show()

def histo_mean():
    master = pd.read_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_array_train.pkl")
    plots = np.load("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_binplots_train_unstandardized.npy")
    labels = np.asarray(master["Ice-Ring"])
    ice_plots, nice_plots = [],[]

    #select I or F
    for i,plot in enumerate(plots):
        if labels[i] == 1 and master["F_o_I"][i] == "F":
            ice_plots.append(plots[i])
        if labels[i] == 0 and master["F_o_I"][i] == "F":
            nice_plots.append(plots[i])

    nice_plots = nice_plots[:len(ice_plots)]

    def stat_hist(lst):
        #transform plot into y-distribution
        y_distr = []
        for element in lst:
            y_sum_plot = []
            for i in range(80):
                y_sum = np.sum(element[i])
                y_sum_plot.append(y_sum)
            y_distr.append(y_sum_plot)
        return y_distr

    def meaner(input_plot):
        #which statistcal parameter
        mean_plot = []
        for plot in input_plot:
            mean_plot.append(scp.iqr(plot))
        return mean_plot

    ice_y_distr = meaner(stat_hist(ice_plots))
    nice_y_distr = meaner(stat_hist(nice_plots))

    bins = np.linspace(0, 80, 20)
    plt.hist(ice_y_distr, bins= bins, alpha=0.8, label="ice ring", color="steelblue", edgecolor="black")
    plt.hist(nice_y_distr, bins= bins, alpha=0.5, label="non ice ring", color="darkseagreen", edgecolor="black")
    plt.legend(loc = "upper right")
    plt.savefig("histo_mean.svg")
    plt.show()

def plot_train():
    model = "m_fobs"
    metric = "loss"
    train = pd.read_csv("/Users/kristophernolte/Documents/Helcaraxe_v2/stats/train_csv/{}/{}_train".format(model,metric))
    val = pd.read_csv("/Users/kristophernolte/Documents/Helcaraxe_v2/stats/train_csv/{}/{}_val".format(model,metric))
    print(train.head())

    def plotter(train, val, y_value):
        fig, ax = plt.subplots()
        ax.plot(train["Value"], color="darkseagreen", label="Train")
        ax.plot(val["Value"], color="steelblue", label="Validation")
        ax.yaxis.grid(color="gray", linestyle="dashed")

        ax.set_xlabel('Epoch')
        ax.set_xticks(np.arange(start=0, stop=len(train), step=2))

        ax.set_yticks(np.arange(start=0.0, stop=1.05, step=0.2))
        ax.set_ylabel(y_value)

        plt.legend()
        plt.show()
    plotter(train, val, y_value="Loss")

def pie_chart():
    fig, ax1 = plt.subplots()
    labels = ["Train", "Validation", "Test"]
    #train,val,test
    vals = np.array([[10585-726, 726], [2457-261, 261], [1411-107, 107]])

    ax1.pie(vals.sum(axis=1), radius=1, colors=["darkseagreen","steelblue","darkslateblue"],labels=labels,
           wedgeprops=dict(width=0.6, edgecolor='black'), autopct='%1.1f%%')
    #ax1.pie(vals.flatten(), radius=1, colors=["darkseagreen","mediumseagreen","steelblue","lightskyblue","darkslateblue","mediumslateblue"],
           #wedgeprops=dict(width=0.7, edgecolor='w'))

    ax1.set(aspect="equal")
    plt.title("Proportion of different data sets")
    plt.savefig("pie_data_distr.svg")
    plt.show()

def bar_chart():
    import numpy as np
    import matplotlib.pyplot as plt

    labels = ['Train', 'Validation', 'Test']
    labels2 =[ "ice-ring","ice-ring","ice-ring"]
    non_ice = [10585-726, 2457-261, 1411-107]
    ice = [726, 261, 107]

    non_ice=[100-6.9,100-10.6,100-7.6]
    ice=[6.9,10.6,7.6]
    width = 0.6  # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    ax.bar(labels, non_ice, width, label='non ice ring',color=["darkseagreen","steelblue","darkslateblue"],edgecolor="black")
    ax.bar(labels, ice, width, bottom=non_ice,color=["lightgreen","lightskyblue","mediumslateblue"],
           label=[6.9,10.6,7.6], edgecolor="black")

    ax.set_ylim(0,120)
    ax.set_yticks(np.arange(0,101,25))
    ax.set_ylabel('Percentage')
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray", linestyle="dashed")
    plt.title("Percentage of ice rings in different data sets")
    plt.savefig("bar_data_distr.svg")
    plt.show()

def error_per_position():
    eva = pd.read_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/evaluation_table_test_Iobs.pkl")
    #eva = pd.read_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/evaluation_table_test_Fobs.pkl")
    eva["diff"] = eva["diff"].astype(float)
    print(eva.info())
    eva["pos"] = np.arange(len(eva))
    for i,element in enumerate(eva["names"]):
        eva["pos"][i] = element[8:]

    print(eva.corr())

    """numbers = np.arange(24)
    for number in numbers:
        temp_lst = []
        where = np.where(eva["pos"]==number)
        for index in where:
            temp_lst.append(np.asarray(eva["diff"][index]))
        print(np.mean(temp_lst),",")"""

def plot_error():
    Ierr = [0.04584906861363822 ,
0.027286586548558225 ,
0.027299484548673075 ,
0.007357358318074603 ,
0.04227092506425123 ,
0.013599913108451784 ,
0.016656724908148884 ,
0.030900961337121727 ,
0.033591002919877155 ,
0.006048897741924233 ,
0.0003082555599070878 ,
0.03847548940107496 ,
0.0015901042527895531 ,
0.06799580625920498 ,
0.00030492267214867754 ,
0.0017074174975277856 ,
0.0016546898223168682 ,
0.0033835631920737796 ,
0.032817463080088295 ,
0.0010393063227335613 ,
0.0013255178928375244 ,
0.00045490264892578125 ,
0.7231247425079346 ,
0.02065005898475647 ]
    Ferr = [0.034962558869234064 ,
0.03309472592383469 ,
0.03410880415851533 ,
0.03279540317613374 ,
0.04593802732415497 ,
0.03463132860504578 ,
0.05625331434574756 ,
0.05568711677702462 ,
0.04326475194737881 ,
0.03037310274023759 ,
0.014814904757908412 ,
0.014477585752805075 ,
0.060747161507606506 ,
0.09110590020815532 ,
0.018673521280288697 ,
0.013924886782964071 ,
0.014560572803020477 ,
0.010843560099601746 ,
0.018895655870437622 ,
0.017855634291966755 ,
0.021260946989059448 ,
0.008979350328445435 ,
0.11603948473930359 ,
0.007967770099639893 ]

    Ierr = Ierr[:20]
    Ferr = Ferr[:20]

    x = np.arange(20)  # the label locations
    width = 0.4  # the width of the bars

    fig, ax = plt.subplots()
    ax.bar(x=x - width/2, height=Ierr, label=r'$\ I_{obs} $', color="darkseagreen", edgecolor="black", width= width)
    ax.bar(x=x + width/2, height=Ferr, label=r'$\ F_{obs} $', color="steelblue", edgecolor="black", width= width)
    ax.set_xticks(x)
    ax.set_ylim([0,0.1])
    ax.set_ylabel('Mean prediction label difference')
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    fig.set_size_inches(10, 5)
    ax.set_axisbelow(True)
    ax.yaxis.grid(color="gray", linestyle="dashed")
    plt.title("Mean Prediction Label difference per position")
    plt.legend()
    plt.savefig("error_p_position.svg")

    plt.show()

error_per_position()