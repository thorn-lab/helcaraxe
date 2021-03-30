from numpy import load
import pandas as pd
import numpy as np
import tensorflow as tf

"""
This code was written by Kristopher Nolte in 2020 as part of Thorn Lab, University of Würzburg.
It loads the pic_arrays and the model then evaluates the models in the pics
"""

model = tf.keras.models.load_model("Helcaraxe_exe/final_models/best_Fobs_model")

#Fobs or Iobs
version = "Iobs"

#load
plots = load("arrays/master_binplots_test_Iobs_cleaned.npy")
master = pd.read_pickle("arrays/master_array_test_{}_cleaned.pkl".format(version))
labels = master["Ice-Ring"]
names = master["name"]
print(len(plots), len(master))

#transform
plots = plots.reshape(len(plots),80,80,1)
plots = np.asarray(plots).astype(np.float32)
labels = np.asarray(labels).astype(np.float32)

#evaluate
#results = model.evaluate(plots, labels)
prediction = model.predict(plots[960:962])
print(prediction)
"""#present
eva_df = pd.DataFrame(columns=["names","labels","prediction","diff"])
eva_df["names"] = names
eva_df["labels"] = labels
eva_df["prediction"] = prediction
for i,label in enumerate(eva_df["labels"]): eva_df["diff"][i] = abs(label-eva_df["prediction"][i])

#save
eva_df.to_pickle("RESULTS/evaluation_table_test_{}.pkl".format(version))
eva_df.to_excel("RESULTS/evaluation_table_test_{}.xlsx".format(version))"""

