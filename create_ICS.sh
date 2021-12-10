#!/usr/bin/env bash

# Script to control the full workflow to create 
# initial conditions from an AMM7 restart file

source set_env.sh

cd ICS
. 1_interp.sh
python 2_create_IC_file.py
python 3_extract_values.py
python 4_convert_bioalk_to_TA.py
cd ..
