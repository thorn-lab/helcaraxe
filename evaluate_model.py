from numpy import load
import pandas as pd
import numpy as np
import tensorflow as tf

"""
This code was written by Kristopher Nolte in 2020 as part of Thorn Lab, University of Würzburg.
It loads the pic_arrays and the model then evaluates the models in the pics
"""
#model = tf.keras.models.load_model("/Users/kristophernolte/Documents/Helcaraxe_v2/model/model_onlyFobs_better.h5")
model = tf.keras.models.load_model("/Users/kristophernolte/Documents/Helcaraxe_v2/model/Helcaraxe_Iobs.h5")

#Fobs or Iobs
version = "Iobs"

#load
plots = load("/Users/kristophernolte/Documents/Helcaraxe_v2/arrays/master_binplots_test_{}_cleaned.npy".format(version))
master = pd.read_pickle("/Users/kristophernolte/Documents/Helcaraxe_v2/arrays/master_array_test_{}_cleaned.pkl".format(version))
labels = master["Ice-Ring"]
names = master["name"]

#transform
plots = plots.reshape(len(plots),80,80,1)
plots = np.asarray(plots).astype(np.float32)
labels = np.asarray(labels).astype(np.float32)

#evaluate
results = model.evaluate(plots, labels)
"""prediction = model.predict(plots)

#present
eva_df = pd.DataFrame(columns=["names","labels","prediction","diff"])
eva_df["names"] = names
eva_df["labels"] = labels
eva_df["prediction"] = prediction
for i,label in enumerate(eva_df["labels"]): eva_df["diff"][i] = abs(label-eva_df["prediction"][i])

#save
eva_df.to_pickle("/Users/kristophernolte/Documents/Helcaraxe_v2/arrays/evaluation_table_test_{}.pkl".format(version))
eva_df.to_excel("/Users/kristophernolte/Documents/Helcaraxe_v2/files/evaluation_table_test_{}.xlsx".format(version))"""

