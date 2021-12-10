#!usr/bin/bash

###############################################
# interp_IC_additional.sh
# This script will perform single interpolation for a variable 
# with a single time record, for variables where the source 
# grid has already had one variable interpolated
###############################################

var=$1       #Input variable name
sfile=$2     #Source file
sourceid=$3  #Source ID Tag

#Fill land values
./sosie3.x -f 1_initcd_${sourceid}_to_${sourceid}_${var}.namelist 

# Create weights
./scripinterp.exe 2_${sourceid}_weights_${var}.namelist

# Fill outerzone
python outerzone/AMM15_outerzone_fill_region.py ${var}

# Fill values
./sosie3.x -f 3_initcd_${sourceid}_to_nemo_${var}.namelist 

