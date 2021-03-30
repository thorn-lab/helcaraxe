import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plots_F = np.load("arrays/Helcaraxe_test_F_plots.npy")
master_F = pd.read_pickle("arrays/master_array_test_Fobs_cleaned.pkl")

plots_I = np.load("arrays/master_binplots_test_Iobs_cleaned.npy")
master_I = pd.read_pickle("arrays/master_array_test_Fobs_cleaned.pkl")

name_lst = np.asarray(master_F["name"])
classification = np.asarray(master_F["Ice-Ring"])

def show_plot(plot, i, FoI):
    plt.imshow(plot)
    plt.title(FoI + str(i)+"_"+name_lst[i]+"_"+str(classification[i]))
    plt.show()
    #plt.savefig("RESULTS/False_fobs/{}.png".format(str(i)+"_"+name_lst[i]+"_"+str(classification[i])))

wrong_lst_I = ['1124', '527', '1112', '1277', '410', '961', '232', '1020', '939',
       '1122', '1380', '1355', '1275', '666', '668', '133', '103', '665',
       '653', '1113', '1312', '769', '1199', '1244', '195', '538', '338',
       '491', '1043', '1365', '234', '1198', '1314', '1196', '216', '973',
       '982', '1197']

wrong_lst_F = ['611', '527', '1272', '133', '666', '1274', '1073', '1195', '1123',
       '981', '1241', '570', '173', '939', '1121', '1112', '234', '1019',
       '665', '769', '923', '532', '811', '309', '972', '812', '810',
       '1362', '297', '892', '1042', '1045', '606', '417', '357']

wrong = [668]
for element in wrong:
    j = element
    show_plot(plots_F[int(element)],int(element),"F")
    show_plot(plots_I[j],int(j),"I")