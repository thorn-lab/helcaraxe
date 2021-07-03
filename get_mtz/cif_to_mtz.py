import os
import requests
import pandas as pd

sf_path = "/Users/kristophernolte/Documents/GitHub/helcaraxe/train_mtz/structure_factors/"
mtz_path = "/Users/kristophernolte/Documents/GitHub/helcaraxe/train_mtz/"

def get_sf (pdb_id):
    pdb_ftp_link = "https://ftp.rcsb.org/pub/pdb/data/structures/all/structure_factors/"
    url = pdb_ftp_link + "r{}sf.ent.gz".format(pdb_id)
    r = requests.get(url)
    with open(sf_path + "r{}sf.cif.gz".format(pdb_id), 'wb') as f:
        f.write(r.content)
    os.system("gunzip "+sf_path + "r{}sf.cif.gz".format(pdb_id))
    return "r{}sf.cif".format(pdb_id)

def convert_sf_to_mtz(filename, pdb_id):
    sf_filepath = sf_path + filename
    mtz_filepath = mtz_path + pdb_id + ".mtz"
    cmd = " ".join(["gemmi", "cif2mtz", sf_filepath, mtz_filepath])
    os.system(cmd)

def main ():
    df = pd.read_pickle("/Users/kristophernolte/Documents/GitHub/helcaraxe/arrays/cleaned_train.pkl")
    pdb_lst = df["PDB-ID"].unique()
    for i,pdb_id in enumerate(pdb_lst):
        pdb_id = pdb_id.replace(" ","")
        pdb_id = pdb_id.lower()
        filename = get_sf(pdb_id)
        convert_sf_to_mtz(filename, pdb_id)
        print(round(i/len(pdb_lst),2))

main()