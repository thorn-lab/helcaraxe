import pandas as pd
import numpy as np
import tensorflow as tf
import Helcaraxe_exe as he

master_array = pd.read_pickle("/Users/kristophernolte/Documents/GitHub/helcaraxe/arrays/master_array_test_Iobs_cleaned.pkl")
pdb_id_lst = master_array["PDB-ID"].unique()

eva_df = pd.DataFrame(columns=["pdb_id","I_name","I_prediction","F_name","F_prediction"])

for j,pdb_id in enumerate(pdb_id_lst):
    print(round(j/len(pdb_id_lst),2))
    mtz_path = "/Users/kristophernolte/Documents/GitHub/helcaraxe/test_mtz/{}.mtz".format(pdb_id)
    I_prediction_lst, F_prediction_lst = he.mtz_opener(mtz_path)
    if I_prediction_lst is not None:
        for i,I_prediction in enumerate(I_prediction_lst):
            if I_prediction != -1:
                I_name = "I__"+pdb_id+"_"+str(i)
                F_name = "F__" + pdb_id + "_" + str(i)
                if F_prediction_lst is not None:
                    if F_prediction_lst[i] != -1:
                        F_prediction = F_prediction_lst[i]
                    else: F_prediction = "resolution range not in mtz"
                else: F_prediction = "no fobs in mtz"
                new_row = {"pdb_id": pdb_id, "I_name": I_name,"I_prediction": I_prediction,"F_name":F_name,"F_prediction":F_prediction}
                eva_df = eva_df.append(new_row, ignore_index=True)


eva_df.to_pickle("elenwe_evaluation_table.pkl")
eva_df.to_excel("elenwe_evaluation_table.xlsx")
