import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
from skimage import io, img_as_float
import tensorflow as tf


root = "/Users/kristophernolte/Documents/Helcaraxe/"
whole = pd.read_pickle("/Users/kristophernolte/Documents/Helcaraxe_v2/arrays/master_array_test_cleaned.pkl")

"""z= 0
counter = 0
for element in whole["Nmbr"]:
    try:
        z += int(element)
        counter += 1
    except ValueError: pass
print(z/counter)
"""
#Ice ring infestation proportion
"""print(whole["Ice-Ring"].value_counts())"""
#Position distribution
"""counts = whole["Nmbr"].value_counts(ascending=False)
for ele in np.asarray(counts): print(ele)
print("______")
counts_perc = whole["Nmbr"].value_counts(ascending=False, normalize=True)
for element in np.asarray(counts_perc): print(round(element,4))"""
#Number of infected IDs
"""IDs = whole["PDB-ID"].unique()
print(len(IDs))
Ice = np.asarray(whole["Ice-Ring"])
liste = []
for ID in IDs:
    counter = 0
    for i, PDB in enumerate(whole["PDB-ID"]):
        if ID == PDB:
            if Ice[i] == 1:
                counter +=1
    if counter > 0: liste.append(ID)
print(len(liste))"""
#Ice ring – Position distribution
numbers = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
Ice = np.asarray(whole["Ice-Ring"])

print(Ice[1] == 1)

for num in numbers:
    counter = 0
    for i, pos in enumerate(whole["Nmbr"]):
        if int(num) == pos:
            if Ice[i] == 1:
                counter += 1
    print(num, counter)

#Plot density distribution
#Density – Ice distribution
#Density – Position distribution
#Density -Position – Ice distribution






