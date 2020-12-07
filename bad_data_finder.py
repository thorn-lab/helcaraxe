import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def show_plot(plot, title):
    plt.imshow(plot)
    plt.title(str(title))
    plt.show()
    plt.close()
    #plt.savefig("/Users/kristophernolte/Documents/del_images/{}.png".format(title))

def bad_data_finder():
    plots = np.load("/Users/kristophernolte/Documents/Helcaraxe_v2/arrays/master_binplots_test_Fobs.npy")
    del_lst = []
    j = 0
    while j in range(len(plots)):
        plot = plots[j]
        i = 0
        step = 8
        while i < 80:
            mean_bin = np.mean(plot[:,i:i+step])
            if mean_bin <= 0.005:
                show_plot(plot,j-1)
                del_lst.append(j)
                j += 1
                break
            i += step
        j += 1
        print(j)
    print(del_lst)


def data_correct():
    master = pd.read_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_array_train_60x60.pkl")
    plots = np.load("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_binplots_train_60x60.npy")
    master = np.asarray(master)

    print(len(master))
    print(len(plots))

    """    #change
    to_zero = [998,339,170]
    for x in to_zero: master[x][5] = 0
    to_one = [1200,1302]
    for x in to_one: master[x][5] = 1"""

    #test-del_lst = [287,1210,1209,1212,1297,1206,1408,1291,342,1213,414,1411,1207,1208,1205,1288,1292,1211,345,1409,1294,1407,1410,1295,1289,1287,1290,1293,866,867,868,967,968,969,1280,1281]
    del_lst = [175, 566, 670, 817, 829, 831, 833, 835, 837, 839, 920, 1393, 1396, 1637, 1641, 1643, 1645, 1648, 1739, 1741, 1743, 1745, 1767, 1982, 1985, 2019, 2023, 2042, 2044, 2046, 2121, 2125, 2584, 2587, 2612, 2677, 3450, 3545, 3764, 3766, 3768, 3770, 3772, 3774, 3776, 3778, 3787, 4091, 4662, 4665, 4723, 4726, 4752, 4887, 4932, 5290, 5430, 5433, 5615, 5617, 5662, 5665, 5913, 5915, 5917, 5937, 5941, 5944, 6088, 6090, 6092, 6094, 6096, 6793, 6795, 6797, 6838, 6840, 6842, 6943, 6969, 7091, 7193, 7195, 7991, 8209, 8211, 8341, 8343, 8369, 8371, 8928, 8930, 8932, 9914, 10902, 10953, 10960, 11111, 11114, 11117, 11319, 11353, 11444, 11447, 11666, 11668, 11670, 11672, 11674, 11676, 11678, 11759, 11761, 11763]
    master = np.delete(master, del_lst, axis=0)
    plots = np.delete(plots, del_lst, axis=0)

    master = pd.DataFrame(master, columns=["index", "name", "F_o_I", "PDB-ID", "Nmbr", "Ice-Ring"])
    print(len(master))
    print(len(plots))
    master.to_pickle("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_array_train_60x60_cleaned.pkl")
    np.save("/Users/kristophernolte/Documents/AG_Thorn/Helcaraxe/arrays/master_binplots_train_60x60_cleaned.npy", plots)

data_correct()

