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

ncatted -a _FillValue,$var,m,d,0 ${sfile}

# Create weights
./scripinterp.exe 2_${sourceid}_weights_${var}.namelist

mv initcd_$var.nc initcd_${var}_filled.nc
# Fill values
./sosie3.x -f 3_initcd_${sourceid}_to_nemo_${var}.namelist 

