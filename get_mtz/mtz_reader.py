import numpy as np
import math
import gemmi
import pandas as pd
from scipy import ndimage

"""
This code was written by Kristopher Nolte in 2020 as part of Thorn Lab, University of Hamburg.
This .py takes I_obs, F_obs and Resolution values and out of this produces plots
of resolution ranges in which ice rings can appear.
You need to change the paths in the main function to the correct inputs. 
A mtz file, a classification list with collumns ["PDB-ID", "Ice", "Position"] and the auspex csv file is required
"""
version = "train"

def mtz_reader (mtz, pdb_id):
    """
    :param mtz: a gemmi variable holding a parsed mtz file
    :param pdb_id: str, PDB-ID
    :return: either a list of Iobs or Fobs
    """
    cI_obs, cF_obs, cres, c2res = [], [], [], []
    max_res = mtz.resolution_high()
    I_obs = mtz.column_with_label('I')
    F_obs = mtz.column_with_label('FP')
    #calculate the resulution
    hkl = mtz.make_miller_array()
    res = mtz.cell.calculate_d_array(hkl)
    #Only use valid values of I and F
    try:
        try:
            #Take I if possible and F if not
                for i,element in enumerate(res):
                    if math.isnan(float(element)) or math.isnan(float(I_obs[i])):
                        pass
                    else:
                        cI_obs.append(I_obs[i])
                        cres.append(element)
                plot(cres, cI_obs, pdb_id, max_res, "I_")
        except (ValueError, TypeError):
            for i, element in enumerate(res):
                if math.isnan(float(element)) or math.isnan(float(F_obs[i])):
                    pass
                else:
                    cF_obs.append(F_obs[i])
                    c2res.append(element)
            plot(c2res, cF_obs, pdb_id, max_res, "F_")
    except TypeError: pass

def plot (res_lst, ampli_lst, pdb_id, max_res, marker):
    """
    :param res_lst: list,  resolution values
    :param ampli_lst: list,  Fobs or Iobs values
    :param pdb_id: str, PDB-ID
    :param max_res: float, maximum resolution
    :param marker: str, F or I
    :return: plot_lst conataining the 2D-histograms, id_lst, list contain
    """
    auspex_rng = np.genfromtxt(root+"Helcaraxe_program/Auspex_ranges.csv", delimiter=';')

    for i, element in enumerate(auspex_rng):
        position = str(i - 1)
        y_range, bin_stat = [], []

        res_bin_start = auspex_rng[i][1]
        res_bin_end = auspex_rng[i][2]

        if max_res < res_bin_end:

            for j, res in enumerate(res_lst):
                if res <= res_bin_start and res >= res_bin_end:
                    y_range.append(ampli_lst[j])
            # [[xmin, xmax][ymin, ymax]]

            try: y_limit = [np.percentile(y_range, 0.5),np.percentile(y_range, 95)]
            except IndexError: y_limit= [0, np.percentile(ampli_lst, 90)]

            image_bin = [res_bin_end, res_bin_start], y_limit

            bin_arr, xedges, yedges = np.histogram2d(res_lst, ampli_lst, range=image_bin, bins=80)
            bin_arr = ndimage.rotate(bin_arr, 90) #rotates the image, only useful for visualization
            id_key = "_".join([marker, pdb_id, position])
            id_list.append(id_key)
            plot_list.append(bin_arr)


def master (plot_list, class_list):
    class_tbl = class_list.to_numpy()

    master_array = pd.DataFrame(columns=["name", "F_o_I", "PDB-ID", "Nmbr", "Ice-Ring", "Size"])
    master_array["name"] = id_list

    for i, row in enumerate(master_array["name"]):
        master_array["F_o_I"][i] = row[0]
        master_array["PDB-ID"][i] = row[3:7]
        master_array["Nmbr"][i] = row[8:]

    # goes through the list of images and checks the classification if it has an ice ring or not
    for n, ID in enumerate(master_array["PDB-ID"]):
        try:
            master_array["Ice-Ring"][n] = 0
            result = np.where(class_tbl == ID)
            position = class_tbl[int(result[0])][2]
            for pos in position:
                if int(pos) == int(master_array["Nmbr"][n]):
                    master_array["Ice-Ring"][n] = 1
        except (TypeError, ValueError): pass

    master_array.to_pickle(root+"arrays/helcaraxe_elenwe_{}.pkl".format(version))
    master_array.to_excel(root+"files/helcaraxe_elenwe_{}.xlsx".format(version))
    np.save(root+"arrays/helcaraxe_elenwe_binplots_{}.npy".format(version),plot_list)

def main():
    global plot_list, id_list, root, class_list
    root = "/Users/kristophernolte/Documents/GitHub/helcaraxe/"
    class_list = pd.read_pickle(root + "arrays/cleaned_train.pkl")
    plot_list, id_list, stat_list_l, stat_list_r, missing_keys = [], [], [], [], []

    for i,key in enumerate(class_list["PDB-ID"]):
        key = key[:4]
        try:
            mtz = gemmi.read_mtz_file("/Users/kristophernolte/Documents/GitHub/helcaraxe/train_mtz/"+key+".mtz")
            mtz_reader(mtz, key)
        except RuntimeError: missing_keys.append(key)
        print(round(i/len(class_list),2))

    print(missing_keys)
    master(plot_list, class_list)

main()
