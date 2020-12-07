import pandas as pd
import math
import unicodedata

"""
This code was written by Kristopher Nolte in 2020 as part of Thorn Lab, University of Würzburg.
The .py has the goal to clean up an excel sheet which holds the classification of ice
"""

root = "/Users/kristophernolte/Documents/Helcaraxe_v2/"
version = "test"

def csv_cleaner():
    #reading the csv
    cleaning_set = pd.read_csv(root+"files/{}_label_sheet.csv".format(version), sep=";", dtype='str')
    #converting all Ice values to 0 or 1
    cleaning_set["Ice"] = cleaning_set["Ice"].fillna(0)
    cleaning_set["Ice"] = cleaning_set["Ice"].replace("ices visible",1)
    cleaning_set["Ice"] = cleaning_set["Ice"].replace("1", 1)
    cleaning_set["Ice"] = cleaning_set["Ice"].str.replace("\xa0", "")
    cleaning_set["Ice"] = cleaning_set["Ice"].replace("0", 0)

    #getting a PDB-ID Norm (lowercase, no spaces and remove "+" because excel keeps adding them"
    cleaning_set["PDB-ID"] = cleaning_set["PDB-ID"].str.replace(" ", "")
    cleaning_set["PDB-ID"] = cleaning_set["PDB-ID"].str.replace("+", "")
    cleaning_set["PDB-ID"] = cleaning_set["PDB-ID"].str.replace("\xa0", "")
    cleaning_set["PDB-ID"] = cleaning_set["PDB-ID"].str.lower()

    #Removin unwanted parts of the Position collum and converting it into a list
    cleaning_set["Position"] = cleaning_set["Position"].str.replace(" ", "")
    cleaning_set["Position"] = cleaning_set["Position"].str.replace("\xa0", "")
    cleaning_set["Position"] = cleaning_set["Position"].str.split(",")
    numpy_set = cleaning_set["Position"].to_numpy()

    for i,row in enumerate(numpy_set):
        try:
            if math.isnan(row):
                numpy_set[i] = 0
        except TypeError:
            for i, element in enumerate(row):
                row[i] = int(element)

    # removing not defined data
    cleaning_set = cleaning_set[cleaning_set["Ice"] != 'data were omitted']

    # removing duplicates
    cleaning_set = cleaning_set.drop_duplicates(subset = "PDB-ID")

    # saving the cleaned up array as pkl and xlsx
    cleaning_set.to_pickle(root+"arrays/cleaned_{}.pkl".format(version))
    cleaning_set.to_excel(root+"files/cleaned_{}.xlsx".format(version))
    print(cleaning_set.info())
    print(cleaning_set.head())

csv_cleaner()