#!/usr/bin/env bash

# Script to control the full workflow to create lateral 
# boundary conditions from WOA18 and GLODAP

source set_env.sh

cd LBC
. 1_interp.sh
python 2_seasonalise_glodap.py

ln -s $DOM_DIR/coordinates.bdy.nc .
ln -s $DOM_DIR/coordinates.skagbdy.nc .

python 3_create_LBC_file.py 3_create_LBC_file_atlantic.yaml
python 4_extract_LBC.py 4_extract_LBC_atlantic.yaml

python 3_create_LBC_file.py 3_create_LBC_file_baltic.yaml
python 4_extract_LBC.py 4_extract_LBC_baltic.yaml

cd ..
