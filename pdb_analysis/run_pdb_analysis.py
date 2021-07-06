import Helcaraxe_program.Helcaraxe_exe as he
import pandas as pd
import numpy as np

def get_helcaraxe (pdb_id):
    def interpret_helcaraxe(pred_list):
        ice_ring_index = np.where(pred_list > 0.5)[0]
        if len(ice_ring_index) > 0:
            main_np.append([pdb_id, ice_ring_index])
            return len(ice_ring_index)
        else:
            return 0

    mtz_path = "/Volumes/My Passport/complete_pdb/mtz/r" + pdb_id.lower() + "sf.mtz"
    I_ice_ring_index, F_ice_ring_index = None, None

    I_prediction_lst, F_prediction_lst = he.mtz_opener(mtz_path)
    try:
        if I_prediction_lst is not None:
            I_ice_ring_index = interpret_helcaraxe(I_prediction_lst)
        if F_prediction_lst is not None:
            F_ice_ring_index = interpret_helcaraxe(F_prediction_lst)
    except Exception as e:
        print(e.message)
    return I_ice_ring_index, F_ice_ring_index

def main ():
    global main_np
    main_df = pd.read_pickle("files/pdb_meta_tab.pkl")
    main_np = list(np.load("files/pdb_ice_tab.npy", allow_pickle=True))
    id_list = main_df["PDB ID"]
    for i, pdb_id in enumerate(id_list):
        try:
            if main_df.loc[pdb_id,"I_ice"] == -1 and main_df.loc[pdb_id,"F_ice"] == -1:
                he_result = get_helcaraxe(pdb_id)
                main_df.at[pdb_id, "I_ice"] = he_result[0]
                main_df.at[pdb_id, "F_ice"] = he_result[1]
                if i % 50 == 0:
                    print(str(round(i/len(id_list),4))+" % done")
                    print(main_df["F_ice"].value_counts())

                    main_df.to_pickle("files/pdb_meta_tab.pkl")
                    np.save("files/pdb_ice_tab.npy", main_np)
        except KeyError: pass
    else:
        pass
        main_df.to_pickle("files/pdb_meta_tab.pkl")
        np.save("files/pdb_ice_tab.npy", main_np)