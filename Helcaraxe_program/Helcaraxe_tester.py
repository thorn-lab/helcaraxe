import pandas as pd
import numpy as np
import tensorflow as tf
import Helcaraxe_exe as he

def main():
    """
    lets the Helcaraxe_exe run over the complete all PDBs  given by master_array"PDB-ID"].unique()
    save the results in evaluation_table.pkl and evaluation_table.xlsx
    """
    master_array = pd.read_pickle("/Users/kristophernolte/Documents/GitHub/helcaraxe/dataframes_n_arrays/helcaraxe_test_labels.pkl")
    pdb_id_lst = master_array["PDB-ID"].unique()

    eva_df = pd.DataFrame(columns=["pdb_id","I_name","I_prediction","F_name","F_prediction"])

    #go through all pdbs
    for j,pdb_id in enumerate(pdb_id_lst):
        print(round(j/len(pdb_id_lst),2))
        #load corresponding mtz
        mtz_path = "/Users/kristophernolte/Documents/GitHub/test_mtz/{}.mtz".format(pdb_id)

        #get prediction from the Helcaraxe_exe as two NumPy arrays
        I_prediction_lst, F_prediction_lst = he.mtz_opener(mtz_path)

        #test set only has I_obs and sometime F_obs therefore when Iobs is not None the mtz file was readable
        if I_prediction_lst is not None:
            #Saves the name for each plot and its prediction
            for i,I_prediction in enumerate(I_prediction_lst):
                if I_prediction != -1:
                    I_name = "I__"+pdb_id+"_"+str(i)
                    F_name = "F__" + pdb_id + "_" + str(i)
                    #checks if F_prediction_lst is available
                    if F_prediction_lst is not None:
                        if F_prediction_lst[i] != -1:
                            F_prediction = F_prediction_lst[i]
                        else: F_prediction = "resolution range not in mtz"
                    else: F_prediction = "no fobs in mtz"
                    #saves results in an array and passes it to the DataFrame
                    new_row = {"pdb_id": pdb_id, "I_name": I_name,"I_prediction": I_prediction,"F_name":F_name,"F_prediction":F_prediction}
                    eva_df = eva_df.append(new_row, ignore_index=True)

    eva_df.to_pickle("evaluation_table.pkl")
    eva_df.to_excel("evaluation_table.xlsx")
