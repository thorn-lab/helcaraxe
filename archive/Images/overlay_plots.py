import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plots = np.load("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_binplots_train.npy")
master = pd.read_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_array_train.pkl")
ice_nice = np.asarray(master["Ice-Ring"])
iobs_fobs = np.asarray(master["name"])
image_lst = []
image_lst2 = []

for i,klasse in enumerate(ice_nice):
    if klasse == 1 and iobs_fobs[i][0] == "I":
        image_lst.append(plots[i])

for i,klasse in enumerate(ice_nice):
    if klasse == 1 and iobs_fobs[i][0] == "F":
        image_lst2.append(plots[i])

mean_plot = np.average(image_lst, axis = 0)
mean_plot2 = np.average(image_lst2, axis = 0)
#mean_plot = np.asarray(mean_plot) - np.asarray(mean_plot2)
plt.imshow(mean_plot)
plt.savefig("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/Images/I_ice_meanplot.svg")
plt.title("Fobs ")
plt.show()
plt.imshow(mean_plot2)
plt.savefig("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/Images/F_ice_meanplot.svg")
plt.show()
