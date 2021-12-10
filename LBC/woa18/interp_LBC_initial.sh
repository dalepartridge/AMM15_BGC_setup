#!usr/bin/bash

###############################################
###############################################

var=$1       #Input variable name
sfile=$2     #Source file
sourceid=$3  #Source ID Tag
stime=$4     #Source time variable

ncatted -a _FillValue,$var,m,d,0 ${sfile}

# Create weights
./scripgrid.exe 2_${sourceid}_weights_${var}.namelist # creates datagrid_file and nemogrid_file
./scrip.exe 2_${sourceid}_weights_${var}.namelist

Nrec=`ncks -M -C -v time $sfile | grep "name = time, size =" | cut -d' ' -f 10`
for i in $(seq 0 $(expr $Nrec - 1));
do
    f=`printf "split_%03d.nc" $i`
    ncks -d time,$i ${var}_${sourceid}-${sourceid}_LBC.nc $f
    sed -i "64 c\ \ \ \ input_file = \"$f\"" 2_${sourceid}_weights_${var}.namelist
    sed -i "74 c\ \ \ \ output_file = \"init_$f\"" 2_${sourceid}_weights_${var}.namelist
    ./scripinterp.exe 2_${sourceid}_weights_${var}.namelist
done
ncrcat init_* initcd_${var}_filled.nc
rm -rf split* init_*

#Create mask
ncks -d time_counter,0,0,1 -v $var initcd_${var}_filled.nc sosie_initcd_mask.nc
ncrename -v $var,mask sosie_initcd_mask.nc
ncap2 -O -s 'where(mask>=0) mask=1' sosie_initcd_mask.nc sosie_initcd_mask.nc

# Fill values
./sosie3.x -f 3_initcd_${sourceid}_to_nemo_${var}.namelist 

