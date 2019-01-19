##########################################################################
#
# Purpose: of this script is to use Chimera to automate making figures
#
##########################################################################
# Open chimera, File > Open, Select this python script 
### Note: to save files you need to make sure there are
# read and write permissions in the folder saving it to
# and provide the path for the folder saving image to
##########################################################################

import os
from chimera import runCommand as rc
from chimera import replyobj
import re

# change to folder with data files
#os.chdir("/Users/vyduong/cloudv/WW/docked_YP_muts/analysis")
path = "/Users/vyduong/cloudv/WW/docked_YP_muts/analysis"

# list of pdb files
file = ['frame_closest_avg.17058.YP_9A.smad7.pdb'
,'frame_closest_avg.199.YP_4-5A.smad7.pdb'
,'frame_closest_avg.26908.YP_33A.smad7.pdb'
,'frame_closest_avg.3544.YP_23A.smad7.pdb'
,'frame_closest_avg.6960.YP_28A.smad7.pdb']

n_WW = 9
n_smad7 = 19

# loop through files
for fn in file: 
	
	n_WW += 1
	n_smad7 += 1

	# variable must be string to work, not int
	numW = str(n_WW)
	numS = str(n_smad7)

	# full path for file
	cpath = "%s/%s" %(path,fn)
	print(cpath)

	# To split string using re.search to get residue number
	result = re.search('YP_(.*)A.smad7.pdb',fn) 
	r = str(result.group(1))
	res = {'4-5':'LP','7':'G','8':'W','9':'E','20':'F','30':'W','33':'P','23':'H','28':'T'}

	# image name and path
	imagefile = "/Users/vyduong/cloudv/WW/pics/figures/2/Mut_complexes/front_YP_%s%s.tiff" %(r,res[r])

	# make copy of pdb
	replyobj.status("Processing " + cpath) # show what file we're working on
	replyobj.status("YP_"+r+"A is mode "+numW) # reply log model
	replyobj.status("smad7_"+r+"A is mode "+numS) # reply log model

	# open fn from file list
	rc("open "+numW+" "+cpath) # need these plus signs to insert variable

	# align to model #2
	rc("mm #2 #"+numW)

	# make a copy of original structure to delete the :1-36 later 
	rc("combine #"+numW+" refSpec #"+numW+" name smad7_"+r+"A modelId "+numS) # copy file  
	rc("del #"+numS+":1-36")
	rc("del #"+numW+":37-50")

	# color smad7 model purple and WW domain green
	rc("modelcolor #33a02c #"+numW)
	rc("modelcolor purple #"+numS)

	# front side
	rc("color hot pink #"+numW+":30")
	rc("color yellow #"+numW+":9,23,28")
	rc("color byhet #"+numW+":9,23,28,30")

	# show residues and hide H atoms
	rc("show #"+numW+":9,23,28,30")
	rc("rep bs #"+numW+":9,23,28,30")
	rc("~show element.H") 

	# show surface and surftransp
	rc("surface #"+numW)
	rc("surftransparency 90")

	# display only selected models
	rc("~modeldisplay")
	rc("modeldisplay #"+numW+","+numS)

	# set background transparent and save figure
	rc("set bgTransparency")
	rc("copy file "+imagefile+" tiff width 3.94457 height 4.0 units inches dpi 400")

	#rc("swapaa ala :"+i+".a") #swapaa command 'swaps' residue e.g. 4 into an alanine 
	#rc("write #0 ~/cloudv/WW/YP-WW/YP_mut_new/YP_"+i+"A.pdb") # write out pdbfile to location

	#rc("close all") #close session

# uncomment to to close chimera session
#rc("close all")

#copy file test.tiff tiff width 3.94457 height 4.0 units inches dpi 400
