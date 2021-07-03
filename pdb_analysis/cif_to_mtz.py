import os
import numpy as np

cif_path = "/Users/kristophernolte/Documents/GitHub/helcaraxe/Helcaraxe_program/mtz/"
mtz_path = "/Users/kristophernolte/Documents/GitHub/helcaraxe/Helcaraxe_program/mtz/"

file_list = ["1rdr-sf.cif"]

for i, filename in enumerate(file_list):
    print(i, len(file_list))
    cif_filepath = cif_path + filename
    mtz_filepath = mtz_path + filename.split(".", 1)[0] + ".mtz"
    cmd = " ".join(["gemmi", "cif2mtz", cif_filepath, mtz_filepath])
    os.system(cmd)