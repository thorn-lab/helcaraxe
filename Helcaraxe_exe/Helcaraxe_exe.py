import numpy as np
import scipy as scp
from tensorflow import keras, image

"""
This code was written by Kristopher Nolte in 2020 as part of Thorn Lab, University of Hamburg.
This .py takes I_obs, F_obs and Resolution values and out of this produces plots
of resolution ranges in which ice rings can appear.
These plots are classified by a CNN model and the prediction is returned as a numpy array
"""

def file_walker(pdb_lst):
    # This is only to test, this task will be taken by auspex !!!
    import math
    import gemmi

    def mtz_reader():
        cI_obs, cF_obs, cres, c2res = [], [], [], []
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
                    cres.append(element)
            return cres, cI_obs

        def get_Fobs():
            for i, element in enumerate(res):
                if math.isnan(float(element)) or math.isnan(float(f_obs[i])):
                    pass
                else:
                    cF_obs.append(f_obs[i])
                    c2res.append(element)
            return cres, cI_obs

        try:
            Icres, cI_obs = get_Iobs()
        except (ValueError, TypeError):
            Icres, cI_obs = None, None

        try:
            Fcres, cF_obs = get_Fobs()
        except TypeError:
            Fcres, cF_obs = None, None

        return main(Icres, Fcres, cI_obs, cF_obs)

    for i, key in enumerate(pdb_lst):
        key = key[:4]
        try:
            mtz = gemmi.read_mtz_file("mtz/" + key + ".mtz")
            return mtz_reader()
        except RuntimeError:
            print("RunTimeError")

def main(i_res, f_res, i_obs, f_obs):
    """
    :param i_obs: list of I_obs values
    :param f_obs: list of F_obs values
    :param res_lst: list of Resolution values
    All parameters have to have the same lenght! The index of the list is used for referencing

    :var model: .h5 file, Convolutional Neural Network (CNN) model, input shape: [80,80,1], output: float between 0 or 1
    :var prediction_lst: list of predictions, index is refering to ice_ranges. Possible Predictions:
        int (-1) = Resolution range was not available
        NoneType (None) = Resolution range was not predicted due to missing intensities
        float (0 -> 1) = classification of the model, 0 = no ice ring, 1 = ice ring
    """
    global model
    ice_ranges = np.genfromtxt("auspex_ranges.csv", delimiter=';')
    model_iobs = keras.models.load_model("Helcaraxe_Iobs.h5")
    model_fobs = keras.models.load_model("Helcaraxe_Fobs.h5")
    I_prediction_lst, F_prediction_lst = None, None

    # Takes I_obs value if avaible when not F_obs values are taken
    if i_obs is not None and i_res is not None:
        model = model_iobs
        I_plot_lst, I_del_list = plot_generator(i_res, i_obs, ice_ranges)
        I_prediction_lst = predictor(I_plot_lst, I_del_list)

    if f_obs is not None and f_res is not None:
        model = model_fobs
        F_plot_lst, F_del_list = plot_generator(f_res, f_obs, ice_ranges)
        F_prediction_lst = predictor(F_plot_lst, F_del_list)

    else:
        raise Exception("Invalid Input")

    if I_prediction_lst is not None:
        if F_prediction_lst is not None:
            return (I_prediction_lst+F_prediction_lst)/2
        else:
            return I_prediction_lst
    else:
        return F_prediction_lst


def plot_generator(res_lst, y_lst, ice_ranges):
    """
    :param res_lst: list of resolution values
    :param y_lst: list of either I_obs or F-obs values
    :param max_res: maximum resolution in which intensities are recorded
    :param ice_ranges: .csv file, holds information about the resolution ranges in which ice rings can appear
    :var plots: 2D array of Intensities against resolution in distinct resolution ranges
    :var y_range: Intensities in the resolution range
    :return: list of plots

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
    plot_lst = np.asarray(plot_lst).astype(np.float32)
    plot_lst = plot_lst.reshape(len(plot_lst), 80, 80, 1)
    plot_lst = image.per_image_standardization(plot_lst)
    return plot_lst, del_lst


def predictor(plot_lst, del_lst):
    """
    :param plot_lst: list of 3D plots, shape: [None,80,80,1]
    :return: predict_dict[PDB_ID], numpy.ndarray
    """
    # iniates prediction_lst
    prediction_lst = np.full([25], -1.0)
    model_prediction = model.predict(plot_lst)

    for j in range(len(model_prediction)):
        if del_lst[j] == 99:
            prediction_lst[j] = None
        else:
            prediction_lst[j] = model_prediction[j][0]

    prediction_lst = np.asarray(np.around(prediction_lst, 2))
    return prediction_lst

print(file_walker(["4n9r"]))
