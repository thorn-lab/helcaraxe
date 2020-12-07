import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

master_array = pd.read_pickle("/arrays/master_array_train.pkl")
name = master_array["name"]
plots = np.load("/arrays/master_binplots_train.npy")
plot_l = np.load("/arrays/master_binstats_train_r.npy")
plot_r = np.load("/arrays/master_binstats_train_l.npy")
del_lst = np.load("/arrays/del_lst.npy")
ice_list = np.asarray(master_array["Ice-Ring"])

i = 12399

while i in range(len(plots)):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
    fig.subplots_adjust(hspace=0)

    ax2.set(title=str(name[i]) + "_" + str(master_array["Ice-Ring"][i]))
    ax1.imshow(plot_l[i])
    ax2.imshow(plots[i])
    ax3.imshow(plot_r[i])

    ax2.set_yticks(np.arange(8, 80, step=8))
    ax2.set_xticks(np.arange(8, 80, step=8))
    ax2.grid(alpha=0.2)

    ax1.tick_params(left = False, bottom=False, labelbottom=False, labelleft=False)
    ax2.tick_params(left = False, bottom=False, labelbottom=False)
    ax3.tick_params(left = False, bottom=False, labelbottom=False)

    if str(master_array["Ice-Ring"][i]) == "1":
        fig.set_facecolor("r")
    else:
        fig.set_facecolor("w")

    fig.show()
    plt.close()

    def inputter(i):
        answer = input(str(i)+" - 0 [no ice], 1[ice], save, - for del:\n")
        if answer == "":
            return
        if answer == "save":
            print(i)
            master_array["Ice-Ring"] = ice_list
            master_array.to_pickle("/Users/kristophernolte/Documents/Helcaraxe_v2/arrays/master_array_train.pkl")
            np.save("/arrays/del_lst.npy", del_lst)
            inputter(i)
            return
        if answer == "0" or answer == "1":
            ice_list[i] = int(answer)
            return
        if answer == "-":
            np.append(del_lst, [i, master_array["name"][i]])
            return
        else:
            print("wrong input please try again")
            inputter(i)
            return
    inputter(i)
    i +=1
