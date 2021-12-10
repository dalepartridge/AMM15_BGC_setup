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

#Create mask file
ncks -d t,0,0,1 -v $var ${sfile} ${sourceid}_mask.nc
ncrename -v $var,mask ${sourceid}_mask.nc
ncap2 -O -s 'where(mask>0) mask=1' ${sourceid}_mask.nc ${sourceid}_mask.nc
ncatted -a _FillValue,mask,m,d,0 ${sourceid}_mask.nc

#Fill land values
./sosie3.x -f 1_initcd_${sourceid}_to_${sourceid}_${var}.namelist 

# Create weights
./scripgrid.exe 2_${sourceid}_weights_${var}.namelist # creates datagrid_file and nemogrid_file
./scrip.exe 2_${sourceid}_weights_${var}.namelist
./scripinterp.exe 2_${sourceid}_weights_${var}.namelist

# Fill outerzone
python outerzone/AMM15_outerzone_fill_region.py ${var}

#Create mask
ncks -d time_counter,0,0,1 -v $var initcd_${var}_filled.nc sosie_initcd_mask.nc
ncrename -v $var,mask sosie_initcd_mask.nc
ncap2 -O -s 'where(mask>=0) mask=1' sosie_initcd_mask.nc sosie_initcd_mask.nc

# Fill values
./sosie3.x -f 3_initcd_${sourceid}_to_nemo_${var}.namelist 

