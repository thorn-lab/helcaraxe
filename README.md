# helcaraxe
"The second element in Helkarakse is said to be the Quenya word karakse ("jagged hedge of spikes"). Helge Fauskanger has suggested that the first element (hel-) derives from the root KHELEK ("ice")." -http://tolkiengateway.net/wiki/Helcarax%C3%AB

The project aims to find ice-rings in protein diffraction data which are visible as "spikes" in plots of structure factor or observed intensity versus resolution.

#NAMING CONVENTIONS
evaluation_table -> results of evaluation against test set
master 		-> complete preprocessed version
binplots 	-> NumPy array which holds the 2D histograms
array 		-> pandas DataFrame holding metadata + labels(accesable ["Ice-Ring])
train 		-> training set(:len(X)*0.8) and validation set(len(X)*0.8:)
Fobs/Iobs	-> histograms have been generated only out of the named value
cleaned 		-> Bad data has been removed.

#FOLDER
arrays: 		.pkl and .npy files which hold data read by the scripts

files: 		.csv and .xlsx files which hold to human readable data

Helcaraxe_programm: contains the final models, deployable script, auspex_ranges and some mtz to test

Env:		contains the environment in which Helcaraxe was developed

Archive: 	contains old files which are not relevant

pdb_analysis:	contains script and data for Helcaraxe pdb run
