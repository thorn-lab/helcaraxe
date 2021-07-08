# helcaraxe
"The second element in Helkarakse is said to be the Quenya word karakse ("jagged hedge of spikes"). Helge Fauskanger has suggested that the first element (hel-) derives from the root KHELEK ("ice")." -http://tolkiengateway.net/wiki/Helcarax%C3%AB

The project aims to find ice-rings in protein diffraction data which are visible as "spikes" in plots of structure factor or observed intensity versus resolution.

#data
ARM: .yml of the environment used

Data: .pkl and .npy files which hold data read by the scripts

Get_mtz/cif_to_mtz.py: script to convert sf.cif files to .mtz

Helcaraxe_programm: contains the final models, deployable script, auspex_ranges, some mtz to test and script which evaluates the performance of the Helcaraxe models

Helcaraxe_module: contains script to be loaded as module into AUSPEX

Ipynb: contains Jupiter notebooks which were used to build and train the model. Also contains a script to prepare helcarxe models to be used in SmoothGrad and a script which lets SmoothGrad run on the model. 

pdb_analysis:	contains script and data for Helcaraxe pdb run
