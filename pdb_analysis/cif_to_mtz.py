import os
import numpy as np

cif_path = "/Volumes/My\ Passport/complete_pdb/sf_unzipped/"
mtz_path = "/Volumes/My\ Passport/complete_pdb/mtz/"

file_list = np.load("files_list.npy")

for i, filename in enumerate(file_list):
    print(i, len(file_list))
    cif_filepath = cif_path + filename
    mtz_filepath = mtz_path + filename.split(".", 1)[0] + ".mtz"
    cmd = " ".join(["gemmi", "cif2mtz", cif_filepath, mtz_filepath])
    os.system(cmd)