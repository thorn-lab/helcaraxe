import pandas as pd
import os

def csv_to_pkl():
    csv_path = "PDB_REPORT_csv/"
    for dirpath, dirnames, files in os.walk(csv_path): pass
    columns=["Entry ID","Collection Temperature","Experimental Method","Matthews Coefficient","Percent Solvent Content","Crystallization Method","pH","Crystal Growth Procedure","Temp (K)","Deposition Date","PDB ID","Resolution (√Ö)","Average B Factor","R Free","R Work","R All","R Observed","High Resolution Limit","Reflections For Refinement","Structure Determination Method"]
    for i, file in enumerate(files):
        main_df = pd.DataFrame(columns=columns)
        csv_file = pd.read_csv(csv_path+os.sep+file, names=columns, error_bad_lines=False)
        main_df = main_df.append(csv_file)
        main_df.to_pickle("PDB_REPORT_pkl/pdb_meta_batch_{}.pkl".format(i))

def pkl_merger():
    pkl_path = "PDB_REPORT_pkl/"
    for dirpath, dirnames, files in os.walk(pkl_path): pass
    columns = ["Entry ID", "Collection Temperature", "Experimental Method", "Matthews Coefficient",
               "Percent Solvent Content", "Crystallization Method", "pH", "Crystal Growth Procedure", "Temp (K)",
               "Deposition Date", "PDB ID", "Resolution (√Ö)", "Average B Factor", "R Free", "R Work", "R All",
               "R Observed", "High Resolution Limit", "Reflections For Refinement", "Structure Determination Method"]
    main_df = pd.DataFrame(columns=columns)
    for file in files:
        pkl_file = pd.read_pickle(pkl_path+os.sep+file)
        main_df = main_df.append(pkl_file)
    print(main_df.dtypes)
    main_df.to_pickle("PDB_REPORT_pkl/pdb_meta_tab.pkl")

pkl_merger()