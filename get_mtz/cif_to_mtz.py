import os
import requests
import pandas as pd

#path to root folders
mtz_path = "/Users/kristophernolte/Documents/GitHub/test_mtz/"
sf_path = "/Users/kristophernolte/Documents/GitHub/missing_sf/"

def get_sf (pdb_id):
    """
    downloads the structure factor file for the given id
    :param pdb_id: pdb entry id as str
    :return: filename of the downloaded sf.cif file as str
    """
    pdb_ftp_link = "https://ftp.rcsb.org/pub/pdb/data/structures/all/structure_factors/"
    url = pdb_ftp_link + "r{}sf.ent.gz".format(pdb_id)
    r = requests.get(url)
    with open(sf_path + "r{}sf.cif.gz".format(pdb_id), 'wb') as f:
        f.write(r.content)
    #unzips the downloaded file
    os.system("gunzip "+sf_path + "r{}sf.cif.gz".format(pdb_id))
    return "r{}sf.cif".format(pdb_id)

def convert_sf_to_mtz(filename, pdb_id):
    """
    :param filename: str name of the file which has to be converted from sf.cif to .mtz
    :param pdb_id: pdb entry id as str
    :return: executes command cif2mtz in gemmi
    """
    sf_filepath = sf_path + filename
    mtz_filepath = mtz_path + pdb_id + ".mtz"
    cmd = " ".join(["gemmi", "cif2mtz", sf_filepath, mtz_filepath])
    os.system(cmd)

def main ():
    """
    for unique pdb entry in DataFrame df it downloads the sf.cif file from the rcsb and then converts it to mtz
    uses the paths to root folders defined at line 6 & 7
    """
    df = pd.read_pickle("/Users/kristophernolte/Documents/GitHub/helcaraxe/arrays/cleaned_train.pkl")
    pdb_lst = df["PDB-ID"].unique()
    for i,pdb_id in enumerate(pdb_lst):
        pdb_id = pdb_id.replace(" ","")
        pdb_id = pdb_id.lower()
        filename = get_sf(pdb_id)
        convert_sf_to_mtz(filename, pdb_id)
        print(round(i/len(pdb_lst),2))

convert_sf_to_mtz("3m9s-sf.cif", "3m9s")