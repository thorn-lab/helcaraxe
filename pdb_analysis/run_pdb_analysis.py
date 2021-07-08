import Helcaraxe_program.Helcaraxe_exe as he
import pandas as pd
import numpy as np

def get_helcaraxe (pdb_id):
    def interpret_helcaraxe(pred_list):
        """
        :param pred_list: 2D - array containing the prediction of the Helcaraxe model
        :return: amount of ice rings predicted to be in diffraction data set
        """
        #get index of plots which were predicted as ice ring contaminated
        ice_ring_index = np.where(pred_list > 0.5)[0]
        if len(ice_ring_index) > 0:
            #save position of ice ring and PDB-ID in numpy array main_np
            main_np.append([pdb_id, ice_ring_index])
            return len(ice_ring_index)
        else:
            return 0

    # load mtz
    mtz_path = "/Volumes/My Passport/complete_pdb/mtz/r" + pdb_id.lower() + "sf.mtz"
    # set default value to None
    I_ice_ring_index, F_ice_ring_index = None, None

    # read mtz file
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
    """
    lets Helcaraxe_exe run over all the PDB-IDs in main_df["PDB ID"] and saves the results in an numpy array (contains information on the position of ice rings )
    and an DataFrame with additional meta data (here only the amount of detected ice rings per diffraction data set ist saved).
    :return:
    """
    global main_np
    main_df = pd.read_pickle("files/pdb_meta_tab.pkl")
    main_np = list(np.load("files/pdb_ice_tab.npy", allow_pickle=True))
    id_list = main_df["PDB ID"]
    for i, pdb_id in enumerate(id_list):
        try:
            # -1 is the default value in main_df["I_ice"] and main_df["F_ice"] and therefore marks not inspected strcutures.
            if main_df.loc[pdb_id,"I_ice"] == -1 and main_df.loc[pdb_id,"F_ice"] == -1:
                he_result = get_helcaraxe(pdb_id)
                main_df.at[pdb_id, "I_ice"] = he_result[0]
                main_df.at[pdb_id, "F_ice"] = he_result[1]
                #quicksave df and numpy array every 50 data sets
                if i % 50 == 0:
                    print(str(round(i/len(id_list),4))+" % done")
                    print(main_df["F_ice"].value_counts())

                    main_df.to_pickle("files/pdb_meta_tab.pkl")
                    np.save("files/pdb_ice_tab.npy", main_np)
        except KeyError: pass
    else:
        # save df and numpy array at the end
        main_df.to_pickle("files/pdb_meta_tab.pkl")
        np.save("files/pdb_ice_tab.npy", main_np)