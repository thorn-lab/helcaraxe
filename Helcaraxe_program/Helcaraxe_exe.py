import numpy as np
import scipy as scp
import math
import gemmi
from tensorflow import keras, image

"""
This code was written by Kristopher Nolte in 2020/2021 as part of Thorn Lab, University of Hamburg.
This .py takes I_obs, F_obs and Resolution values and out of this produces plots
of resolution ranges in which ice rings can appear.
These plots are classified by a CNN model and the prediction is returned as a numpy array
"""
def mtz_opener(mtz_path):
    """
    Function is only for testing until Helcaraxe is integrated into AUSPEX.py
    opens the mtz file through gemmi.
    :param mtz_path: path as string to .mtz file
    :return: mtz_reader()
    """

    # This is only to test, this task will be taken by auspex !!!
    def mtz_reader():
        """
        Function is only for testing until Helcaraxe is integrated into AUSPEX.py
        gets observed Intensities, observed strcuture factor amplitudes and resolution out of .mtz file
        :return: get_prediction_list
        """
        cI_obs, cF_obs, cI_res, cF_res = [], [], [], []
        i_obs = mtz.column_with_label('I')
        f_obs = mtz.column_with_label('FP')
        hkl = mtz.make_miller_array()
        res = mtz.cell.calculate_d_array(hkl)

        def get_Iobs():
            for i, element in enumerate(res):
                if math.isnan(float(element)) or math.isnan(float(i_obs[i])):
                    pass
                else:
                    cI_obs.append(i_obs[i])
                    cI_res.append(element)
            return cI_res, cI_obs

        def get_Fobs():
            for i, element in enumerate(res):
                if math.isnan(float(element)) or math.isnan(float(f_obs[i])):
                    pass
                else:
                    cF_obs.append(f_obs[i])
                    cF_res.append(element)
            return cF_res, cF_obs

        try:
            cI_res, cI_obs = get_Iobs()
        except TypeError:
            cI_res, cI_obs = None, None

        try:
            cF_res, cF_obs = get_Fobs()
        except TypeError:
            cF_res, cF_obs = None, None

        return get_pred_lst(cI_res, cF_res, cI_obs, cF_obs)

    try:
        mtz = gemmi.read_mtz_file(mtz_path)
        return mtz_reader()
    except RuntimeError:
        raise Exception ("Invalid Input: .mtz file not readable or {} path is wrong".format(mtz_path))

def get_pred_lst (i_res, f_res, i_obs, f_obs):
    """
    :param i_res: list of Resolution values corresponding to i_obs values
    :param f_res: list of Resolution values corresponding to f_obs values
    :param i_obs: list of I_obs values
    :param f_obs: list of F_obs values

    All parameters have to have the same lenght! The index of the list is used for referencing

    :var model: Convolutional Neural Network (CNN) model, input shape: [80,80,1], output: float between 0 or 1
    :var prediction_lst: list of predictions, index is refering to ice_ranges. Possible Predictions:
        int (-1) = Resolution range was not available
        NoneType (None) = Resolution range was not predicted due to missing intensities
        float (0 -> 1) = classification of the model, 0 = no ice ring, 1 = ice ring
    """
    global model, ice_ranges
    #loading resolution ranges and models
    ice_ranges = np.genfromtxt("/Users/kristophernolte/Documents/GitHub/helcaraxe/Helcaraxe_program/Auspex_ranges.csv", delimiter=';')

    model_iobs = keras.models.load_model("/Users/kristophernolte/Documents/GitHub/helcaraxe/Helcaraxe_program/models/Helcaraxe_Fobs_model")
    model_fobs = keras.models.load_model("/Users/kristophernolte/Documents/GitHub/helcaraxe/Helcaraxe_program/models/Helcaraxe_Iobs_model")
    I_prediction_lst, F_prediction_lst = None, None

    # Raises Exception if .mtz file has no f_obs or i_obs values
    if f_obs is None and i_obs is None:
        raise Exception("Invalid Input")

    # Takes I_obs value if avaible and returns list of models prediction
    # ToDo: functionalize
    if i_obs is not None and i_res is not None:
        model = model_iobs
        I_plot_lst, I_del_list = plot_generator(i_res, i_obs, ice_ranges)
        if I_plot_lst is not None and I_del_list is not None:
            I_prediction_lst = predictor(I_plot_lst, I_del_list)
        else:
            raise Exception("Invalid Input")

    # Takes F_obs value if avaible and returns list of models prediction
    if f_obs is not None and f_res is not None:
        model = model_fobs
        F_plot_lst, F_del_list = plot_generator(f_res, f_obs, ice_ranges)
        if F_plot_lst is not None and F_del_list is not None:
            F_prediction_lst = predictor(F_plot_lst, F_del_list)
        else:
            raise Exception("Invalid Input")
    return I_prediction_lst, F_prediction_lst

def plot_generator(res_lst, y_lst, ice_ranges):
    """
    create 2D histograms using intensity (or structure factor)values and resolution
    :param res_lst: list of resolution values
    :param y_lst: list of either I_obs or F-obs values
    :param max_res: maximum resolution in which intensities are recorded
    :param ice_ranges: .csv file, holds information about the resolution ranges in which ice rings can appear
    :var plots: 2D array of Intensities against resolution in distinct resolution ranges
    :var y_range: Intensities in the resolution range
    :return: list of 2D histograms
    """
    plot_lst = []
    del_lst = np.full([25], -1)
    max_res = min(res_lst)

    for pos, range in enumerate(ice_ranges):
        y_range = []

        # set resolution range
        res_bin_start = ice_ranges[pos][1]
        res_bin_end = ice_ranges[pos][2]

        if max_res < res_bin_end:
            for j, res in enumerate(res_lst):
                if res <= res_bin_start and res >= res_bin_end:
                    y_range.append(y_lst[j])

            try:
                y_limit = [np.percentile(y_range, 0.5), np.percentile(y_range, 95)]
            except IndexError:
                y_limit = [0, np.percentile(y_lst, 90)]

            # bin of resolution is set -> [xmin, xmax][ymin, ymax]
            image_bin = [res_bin_end, res_bin_start], y_limit

            # create a 2D histogram of the resolution range
            bin_arr, xedges, yedges = np.histogram2d(res_lst, y_lst, range=image_bin, bins=80)
            bin_arr = scp.ndimage.rotate(bin_arr, 90)

            def discriminator(plot, pos):
                """
                :param plot: 2D array of intensities against resolution
                :param pos: index of resolution range
                :return: sets blank images to None in prediction_lst -> They will not be predicted by the model
                """
                step = 10
                i = 10
                while i < 70:
                    if np.mean(plot[:, i:i + step]) <= 0:
                        del_lst[pos-1] = 99
                        break
                    i += 4
                return del_lst

            del_list = discriminator(bin_arr, pos)
            plot_lst.append(bin_arr)

    # plots are reshaped in a CNN usable format and standardized
    if len(plot_lst) > 0:
        plot_lst = np.asarray(plot_lst)
        plot_lst = plot_lst.reshape(len(plot_lst), 80, 80, 1)
        plot_lst = image.per_image_standardization(plot_lst)
        return plot_lst, del_lst
    else:
        return None, None

def predictor(plot_lst, del_lst):
    """
    calls a helcarxe model for prediction
    :param plot_lst: list of 3D plots, shape: [None,80,80,1]
    :return: predict_dict[PDB_ID], numpy.ndarray
    """
    # iniates prediction_lst
    prediction_lst = np.full([25], -1.0)
    model_prediction = model(plot_lst)
    #checking if discriminator function has marked a histogram and if so sets its value in the prediction list to None
    for j in range(len(model_prediction)):
        if del_lst[j] == 99:
            prediction_lst[j] = 99
        else:
            prediction_lst[j] = model_prediction[j][0]

    prediction_lst = np.asarray(np.around(prediction_lst, 4))
    return prediction_lst

def get_txt(entry_path):
    """
    function for Helcaraxe to be used in the CSTF validation pipeline
    :param entry_path: path to id in repository (example_path = "/Volumes/cstf-repo/coronavirus_structural_task_force/pdb/nsp3/SARS-CoV-2/5rud")
    writes a txt doc in validation folder containing the prediction of Helcaraxe
    """
    id = entry_path[-4:]
    #path to the mtz file correct mtz file
    mtz_path = "/".join([entry_path,"validation", "auspex", "{}-sf.mtz".format(id)])
    #get prediction from model
    pred_lst_I, pred_lst_F = mtz_opener(mtz_path)

    #write .txt doc with with a readable output
    doc = open("/".join([entry_path, "validation","auspex","{}_Helcaraxe_icering_detection.txt".format(id)]), "w+")
    doc.write("###ice crystal artefact detection through Helcaraxe###\n")

    def txt_writer (pred_lst):
        ice_ring_index = np.where(pred_lst > 0.5)
        ice_ring_index = np.squeeze(ice_ring_index)

        if len(ice_ring_index) > 0:
            for i in ice_ring_index:
                startA = ice_ranges[i+1][2]
                endA = ice_ranges[i+1][1]
                prediction = round(pred_lst[i],2)
                doc.write("< {} - {} Å > ice crystal artefact detected, probability: {}\n".format(startA,endA,prediction))
        else:
            doc.write("< no ice crystal artefact detected >\n")

    doc.write("\n-observed intensity data-\n")
    if pred_lst_I is not None:
        txt_writer(pred_lst_I)
    else: pass
    doc.write("\n-structure factor amplitude data-\n")
    if pred_lst_F is not None:
        txt_writer(pred_lst_F)
    else: pass
    doc.close()