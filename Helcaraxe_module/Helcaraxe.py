import numpy as np
import scipy as scp
from tensorflow import keras, image, convert_to_tensor

"""
This code was written by Kristopher Nolte in 2020/2021 as part of Thorn Lab, University of Hamburg.
This .py takes I_obs, F_obs and Resolution values and out of this produces plots
of resolution ranges in which ice rings can appear.
These plots are classified by a CNN model and the prediction is returned as a numpy array
"""

def main (i_res, i_obs, f_res, f_obs):
    """
    :param i_res: list of Resolution values corresponding to i_obs values
    :param i_obs: list of I_obs values
    :param f_res: list of Resolution values corresponding to f_obs values
    :param f_obs: list of F_obs values

    All parameters have to have the same lenght! The index of the list is relevant.

    :var model: Convolutional Neural Network (CNN) model, input shape: [80,80,1], output: float between 0 or 1
    :return[0] I_prediction_lst: list of predictions, index is refering to ice_ranges.
    :return[1] F_prediction_lst: list of predictions, index is refering to ice_ranges.
     Possible Predictions:
        int (-1) = Resolution range was not available
        NoneType (None) = Resolution range was not predicted due to missing intensities
        float (0 -> 1) = classification of the model, 0 = no ice ring, 1 = ice ring
    """

    global model, ice_ranges
    #loading resolution ranges and models
    ice_ranges = np.genfromtxt("Auspex_ranges.csv", delimiter=';')
    model_iobs = keras.models.load_model("final_models/best_Iobs_model")
    model_fobs = keras.models.load_model("final_models/best_Fobs_model")
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
                i = 0
                while i < 80:
                    if np.mean(plot[:, i:i + step]) <= 0.005:
                        del_lst[pos-1] = 99
                        break
                    i += 5
                return del_lst

            del_list = discriminator(bin_arr, pos)
            plot_lst.append(bin_arr)

    # plots are reshaped in a CNN usable format and standardized
    if len(plot_lst) > 0:
        plot_lst = np.asarray(plot_lst).astype(np.float32)
        plot_lst = plot_lst.reshape(len(plot_lst), 80, 80, 1)
        plot_lst = image.per_image_standardization(plot_lst)
        plot_lst = convert_to_tensor(plot_lst)
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
            prediction_lst[j] = None
        else:
            prediction_lst[j] = model_prediction[j][0]
    prediction_lst = np.asarray(np.around(prediction_lst, 2))
    return prediction_lst