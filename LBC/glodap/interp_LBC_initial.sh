#!usr/bin/bash

###############################################
# interp_IC_initial.sh
# This script will perform single interpolation for a variable 
# with a single time record, for the first variable from a source
###############################################

var=$1       #Input variable name
sfile=$2     #Source file
sourceid=$3  #Source ID Tag
stime=$4     #Source time variable

ncatted -a _FillValue,$var,m,d,0 ${sfile}

# Create weights
./scripgrid.exe 2_${sourceid}_weights_${var}.namelist # creates datagrid_file and nemogrid_file
./scrip.exe 2_${sourceid}_weights_${var}.namelist
./scripinterp.exe 2_${sourceid}_weights_${var}.namelist

#Create mask
mv initcd_$var.nc initcd_${var}_filled.nc
ncks -d time_counter,0,0,1 -v $var initcd_${var}_filled.nc sosie_initcd_mask.nc
ncrename -v $var,mask sosie_initcd_mask.nc
ncap2 -O -s 'where(mask>=0) mask=1' sosie_initcd_mask.nc sosie_initcd_mask.nc

# Fill values
./sosie3.x -f 3_initcd_${sourceid}_to_nemo_${var}.namelist 

