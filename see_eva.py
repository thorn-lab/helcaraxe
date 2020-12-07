import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

plots = np.load("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_binplots_test_Fobs_cleaned.npy")
master = pd.read_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_array_test_Iobs.pkl")
name_lst = np.asarray(master["name"])
classification = np.asarray(master["Ice-Ring"])

def show_plot(plot, i):
    plt.imshow(plot)
    #plt.title(str(i)+"_"+name_lst[i]+"_"+str(classification[i]))
    #plt.colorbar()
    plt.savefig("{}_fig21.svg".format(i))
    plt.show()

wrong_lst = [1109]
for element in wrong_lst:
    show_plot(plots[element],element)
