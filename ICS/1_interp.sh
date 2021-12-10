#!/usr/bin/env bash

# Perform interpolation of pelagic and benthic variables from 
# AMM7 restart file. Sets up links to relevant files and 
# calls python scripts in AMM7/ directory to run interpolation

module load nco
source ../set_env.sh
template_dir=../TOOLS/interp-files/namelist-templates/

cd AMM7
cp $EXE_DIR/{scripgrid.exe,scrip.exe,scripinterp.exe} .
cp $EXE_DIR/sosie3.x .
ln -s $DOM_DIR/mesh_mask.nc .
ln -s $SOURCE_DIR/amm7_restart_trc.nc .


python interp_amm7_pelagic.py $template_dir > pelagic_interp.log
mkdir pelagic
mv *.namelist initcd*nc *IC.nc pelagic_interp.log remap*nc sosie*nc AMM7_mask.nc data*nc pelagic/ 

python interp_amm7_benthic.py $template_dir > benthic_interp.log
mkdir benthic
mv *.namelist initcd*nc *IC.nc benthic_interp.log remap*nc sosie*nc AMM7_mask.nc data*nc benthic/ 

mkdir $OUT_DIR/ICS
cd ..
