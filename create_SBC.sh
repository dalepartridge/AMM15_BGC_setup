#!/usr/bin/env bash

# Script to control the full workflow to create surface forcing
# from EMEP (Nitrogen Deposition) and OC-CCI (ADY)

source set_env.sh

mkdir $OUT_DIR/SBC
cd SBC
ln -s $DOM_DIR/mesh_mask.nc .
python create_Ndep_from_EMEP.py
python create_ADY_from_CCI.py
cd ..
